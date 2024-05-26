import axios from "axios";

export function getNews() {
    return axios.get('http://localhost:8000/api/news_feed/news/')
    .then(response => response.data.results);
}

export function getFollowContent(question) {
    const data = {
        question: question
    }
    return axios.post('http://localhost:8000/api/generate/follow/', data)
    .then(response => {
        console.log(response.data);
        return response.data;
    });
}

