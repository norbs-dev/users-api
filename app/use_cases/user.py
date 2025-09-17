from fastapi import status
from typing import List
from sqlalchemy import func, case
from sqlalchemy.exc import IntegrityError
from app.db.models import Users as UserModel
from app.db.models import Projects, Team, Logs
from sqlalchemy.orm import Session
from app.schemas.user import Users
from app.schemas.team import TeamInsight
from app.schemas.responses import ResponseBody, Response
from fastapi.encoders import jsonable_encoder


class UserUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session


    def _build_users_models(self, user: Users):
         projects = [Projects(**projects.model_dump()) for projects in user.team.projects]
         team = Team(name=user.team.name, leader=user.team.leader, projects=projects)
         logs = [Logs(**log.model_dump()) for log in user.logs]
         return UserModel(
                 id=user.id,
                 name=user.name,
                 age=user.age,
                 score=user.score,
                 active=user.active,
                 country=user.country,
                 logs=logs,
                 team=[team]
         )


    def _serialize_user(self, user: UserModel):
         user_model_json = jsonable_encoder(user)
         user_model_json['team'] = user_model_json['team'][0]
         return Users(**user_model_json)
    

    def _encode_json_response(self, response: Response):
         return jsonable_encoder(response.model_dump(exclude_none=True))
    

    def _chunk_users(self, users_list: List, chunk_size: int):
        for i in range(0, len(users_list), chunk_size):
             yield users_list[i:i +chunk_size]


    def add_users(self, users: list[Users]):
        response = {
            "status": status.HTTP_201_CREATED,
            "body": {
                "message": "Arquivo processado com sucesso",
                "users_count": 0
            }
        }
        total_added = 0
        try:
            for chunk in self._chunk_users(users, chunk_size=1000):
                users_models = [
                    self._build_users_models(user) for user in chunk
                ]
                with self.db_session.begin():
                        self.db_session.add_all(users_models)
                print(total_added, 'users added')
                total_added += len(users_models)
        except IntegrityError as err:
            response['body']['message'] = str(err)
            response['body']['users_count'] = 0
            response['status'] = status.HTTP_400_BAD_REQUEST
        response['body']['users_count'] = total_added
        return response


    def get_superusers(self):
        supersusers = self.db_session.query(UserModel).filter(
             UserModel.score >= 900,
             UserModel.active == True
             ).all()
        response_body = ResponseBody(data=supersusers)
        response = Response(status=status.HTTP_200_OK, body=response_body)
        return self._encode_json_response(response)


    def get_top_countries(self):
        top_5_countries = self.db_session.query(UserModel.country,
                                            func.count(UserModel.id)
                                            ).group_by(UserModel.country).order_by(func.count(UserModel.id).desc()).all()[:5]
        top_5_countries_data = [{"country": result[0], "total": result[1]} for result in top_5_countries]
        response_body = ResponseBody(countries=top_5_countries_data)
        response = Response(status=status.HTTP_200_OK, body=response_body)
        return self._encode_json_response(response)


    def get_team_insights(self):
         team_insights = self.db_session.query(Team.name,
                                               func.count(Team.user_id).label("total_members"),
                                               func.sum(case((Team.leader == True, 1), else_=0)).label("leaders"),
                                               func.sum(case((Projects.completed == True, 1), else_=0)).label("completed_projects"),
                                               ((func.sum(case((UserModel.active == True, 1), else_=0)) / func.count(Team.user_id)) * 100).label("active_percentage"),
                                                ).join(UserModel, Team.user_id == UserModel.id).join(Projects, Team.user_id == Projects.user_id).group_by(Team.name).all()
         teams_insights_data = [TeamInsight(**team._asdict()) for team in team_insights]
         response_body = ResponseBody(teams=teams_insights_data)
         response = Response(status=status.HTTP_200_OK, body=response_body)
         return self._encode_json_response(response)

    

    def get_active_users_per_date(self):
         total_logins_per_date = self.db_session.query(Logs.date,
                                                       func.count(Logs.action).label("total")
                                                       ).filter(Logs.action == "login").group_by(Logs.date).all()
         logs_output = [{"date": log[0], "total": log[1]} for log in total_logins_per_date]
         response_body = ResponseBody(logins=logs_output)
         response = Response(status=status.HTTP_200_OK, body=response_body)
         return self._encode_json_response(response)