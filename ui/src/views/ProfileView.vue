<template>
  <div>
      <div class="dashboard-link">
      <router-link :to="{ name: 'dashboard' }">Dashboard</router-link>
    </div>
      <div>
      <router-link :to="{ name: 'UpdateProfile', params: { id: user.id } }">Update Profile | </router-link>
      <button @click="deleteProfile">Delete Profile</button>
    </div>
    <h2><u>Profile Page</u></h2>
    <h2>Name : {{ user.name }}</h2>
    <h3>Username : {{ user.username }}</h3>
    <p>Number of posts created: {{ posts.length }}</p>
    <p>Number of Followers: {{ followers }}</p>
    <p>Number of Following: {{ following }}</p>

    <h3>Posts</h3>
    <ul>
      <li v-for="(post, index) in posts" :key="index">
        <h4>Title : {{ post.title }}</h4>
        <p>Description : {{ post.description }}</p>
        <img :src="require('@/assets/static/uploads/' + post.image_url)" style="max-width: 400px; max-height: 400px;">
        <p>Posted on {{ post.timestamp }}</p>
        <div>
          <router-link :to="{ name: 'UpdatePost', params: { id: post.id } }">Update | </router-link>
          <router-link :to="{ name: 'DeletePost', params: { id: post.id } }"> Delete</router-link>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      user: {},
      posts: [],
      followers: [],
      following: []
    };
  },
  created() {
    this.getUserData();
  },
  methods: {
    async getUserData() {
      try {
        const response = await axios.get(`http://localhost:5000/api/users/${sessionStorage.getItem("userId")}`);
        this.user = response.data;
        this.posts = response.data.blog_posts;
        this.followers = response.data.num_followers;
        this.following = response.data.num_following;
      } catch (error) {
        console.error(error);
      }
    },
    async deleteProfile() {
        try {
            const response = await axios.delete(`http://localhost:5000/api/users/${sessionStorage.getItem("userId")}`);
            console.log(response.data);
            sessionStorage.clear();
            this.$router.push('/');
        } catch (error) {
            console.error(error);
        }
    }
  }
};
</script>
