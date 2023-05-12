import axios from 'axios'

const API_URL = 'http://localhost:5000'

export function getPosts() {
    return axios.get(`${API_URL}/posts`)
}