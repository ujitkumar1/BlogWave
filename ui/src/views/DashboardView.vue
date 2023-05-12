<template>
  <div>
    <h1>Welcome, {{ user.name }}!</h1>
    <p>Your username is: {{ user.username }}</p>
    <button @click="$router.push('/createposts')">Create Post</button>
<button @click="exportAsCsv">Export Posts</button>
    <div v-if="posts.length">
      <h2>Post of Following Users:</h2>
      <ol>
  <li v-for="post in posts" :key="post.id">
      <router-link :to="{ name: 'UserView', params: { username: post.username } }">
        <u><h4>User: {{post.username}}</h4></u>
    </router-link>
    <h4>Title: {{ post.title }}</h4>
    <p><b>Description:</b> {{ post.description }}</p>
    <p><b>Image:</b></p>
    <img :src="require('@/assets/static/uploads/' + post.image_url)" style="max-width: 400px; max-height: 400px;">
      <p>Posted at : {{post.timestamp}}</p>

  </li>
</ol>
    </div>
    <div v-else>
      <p>You are Not following any user, Click on Search user to follow other users.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      user: null,
      name:null,
      posts: []
    }
  },
  mounted() {
    this.user = {
      name: sessionStorage.getItem('name'),
      username: sessionStorage.getItem('username'),
    }
    this.getPosts()
  },
  methods: {
   async getPosts() {
  try {
    const userResponse = await axios.get(`http://localhost:5000/users?username=${this.user.username}`, {
      headers: {
        'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
      },
    });
    const userId = userResponse.data.id;
    console.log(userId)
    const followingResponse = await axios.get(`http://localhost:5000/following_posts?username=${this.user.username}`, {
      headers: {
        'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
      },
    });
    console.log(followingResponse)
    this.posts = followingResponse.data
      console.log(this.posts)
  } catch (error) {
    console.log(error)
  }
},
    async deletePost(postId) {
      try {
        const response = await axios.delete(`http://localhost:5000/posts/${postId}`, {
          headers: {
            'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
          },
        });
        console.log(response.data);
        this.getPosts();
      } catch (error) {
        console.log(error);
      }
    },
      async exportAsCsv() {
  try {
        const response = await axios.get('http://localhost:5000/export_csv', {
    params: {
      user_id: sessionStorage.getItem("userId") // include the user id in the request
    },
          headers: {
            'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
          },
          responseType: 'blob',
        });

    const blob = new Blob([response.data], { type: 'text' });

    const url = URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = url;
    link.download = 'blog_data.txt';

    document.body.appendChild(link);
    link.click();

    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    alert('Export CSV job is completed! and filed save at'+" static/exportJob/blogs.csv");
  } catch (error) {
    console.log(error);
    alert('Export CSV job failed.');
  }
}

  }
}
</script>

<style>
.dashboard {
  margin: 20px;
}

.post-image {
  position: relative;
  display: inline-block;
}

.post-image-actions {
  position: absolute;
  top: 5px;
  right: 5px;
  display: flex;
  flex-direction: column;
}

.post-image-actions button {
  margin-top: 5px;
}

/* added styles for bright colors */

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

.post-image img {
  max-width: 400px;
  max-height: 400px;
  border: 1px solid #0066FF;
  border-radius: 5px;
  padding: 10px;
}

.post-image img:hover {
    border-color: #FF69B4;
}

</style>
