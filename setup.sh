mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"ntihemuka_joel@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[theme]
backgroundColor='#fbfff0'

[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
