mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
maxUploadSize = 10\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml