<template>
  <div>
    <h2><u>Profile Page</u></h2>
    <h2>Name : {{ user.name }}</h2>
    <h3>Username : {{ user.username }}</h3>
    <p>Number of posts created: {{ posts.length }}</p>
    <p>Number of Followers: {{ user.followers_no }}</p>
    <p>Number of Following: {{ user.following }}</p>

    <h3>Posts</h3>
    <ul>
      <li v-for="(post, index) in posts" :key="index">
        <h4>Title : {{ post.title }}</h4>
        <p>Description : {{ post.description }}</p>
        <img :src="require('@/assets/static/uploads/' + post.image_url)" style="max-width: 400px; max-height: 400px;">
        <p>Posted on {{ post.timestamp }}</p>
      </li>
    </ul>
  </div>
</template>


<script>
import axios from 'axios'

export default {
  data() {
    return {
      user: null,
      posts: [],
    }
  },
  mounted() {
    this.getUser()
    this.getPosts()
  },
  methods: {
    async getUser() {
      try {
        const response = await axios.get(`http://localhost:5000/user/${this.$route.params.username}`, {
          headers: {
            'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
          },
        });
        this.user = response.data;
      } catch (error) {
        console.log(error);
      }
    },
    async getPosts() {
      try {
        const response = await axios.get(`http://localhost:5000/posts?username=${this.$route.params.username}`, {
          headers: {
            'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
          },
        });
        this.posts = response.data;
      } catch (error) {
        console.log(error);
      }
    },
  }
}
</script>

<style>

h1, h2, h3 {
  color: #FF69B4;
}

p {
  color: #0066FF;
}

button {
  background-color: #FFA500;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  margin-top: 10px;
}

button:hover {
  background-color: #FFC300;
}

ol {
  margin-top: 20px;
}

li {
  margin-top: 20px;
  border: 1px solid #FF69B4;
  border-radius: 5px;
  padding: 10px;
}

li:hover {
  background-color: #FF69B4;
  color: white;
}

img {
  max-width: 400px;
  max-height: 400px;
  border: 1px solid #0066FF;
  border-radius: 5px;
  padding: 10px;
}

img:hover {
  border-color: #FF69B4;
}
</style>
