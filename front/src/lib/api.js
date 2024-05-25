import axios from "axios";

export function getNews() {
    return axios.get('http://localhost:8000/api/news_feed/news/')
    .then(response => response.data.results);
}