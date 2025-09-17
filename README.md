# users-api
API to process and analyze user data.
This app was developed as a study project inspired by the challenge presented in the video:
"UMA API PARA ANALISAR DADOS DE 100 MIL USUÁRIOS - 1 sênior vs. 3 júniors - Codecon"
("ONE API TO ANALYZE DATA FROM 100K USERS - 1 Senior vs. 3 Juniors").
Link to the video: https://www.youtube.com/watch?v=AFtRYXJVO-4&t=1060s


## How to run
Build the docker image by running `docker build -t users-api .` and run the app by runnig `docker run -p 8000:8000 users-api`

## Endpoints
You can access the swagger documentation by going to `http://localhost:8000/docs` and check all the available endpoints.
<img width="1794" height="429" alt="image" src="https://github.com/user-attachments/assets/c6f9e8ad-3a39-4ace-85b2-68f40ed2f376" />

## Test data
The `usarios.json` has all the 100000 user to be sended to the API. You can run the `post_users.py` script to do it. If you want to test with a less amount of users, ther is also the `usuarios_1000.json` with just 1000 users.
