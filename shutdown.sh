ps -aux | grep python| awk '{print $2}' | xargs kill -9
