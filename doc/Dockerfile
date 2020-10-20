FROM nginx

RUN mkdir /usr/share/nginx/html/_static 
COPY docs/_build/*.html /usr/share/nginx/html/
COPY docs/_build/*.js /usr/share/nginx/html/
COPY docs/_build/_static /usr/share/nginx/html/_static/
COPY docs/_build/_images /usr/share/nginx/html/_images/
COPY docs/_build/_downloads /usr/share/nginx/html/_downloads/

