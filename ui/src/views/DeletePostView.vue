<template>
  <div>
    <h2>Delete Post</h2>
    <p>Are you sure you want to delete this post?</p>
    <div>
      <h3>Title: {{ post.name }}</h3>
      <p><b>Description:</b> {{ post.description }}</p>
      <p><b>Image:</b></p>
      <img :src="require('@/assets/static/uploads/'+post.image_url)" style="max-width: 400px; max-height: 400px;">
    </div>
    <button @click="deletePost">Delete Post</button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'DeletePostView',
  data() {
    return {
      post: null
    }
  },
  async created() {
    try {
      const response = await axios.get(`http://localhost:5000/posts/${this.$route.params.id}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });
      this.post = response.data
    } catch (error) {
      console.log(error);
    }
  },
  methods: {
    async deletePost() {
      try {
        await axios.delete(`http://localhost:5000/posts/${this.post.id}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
        });
        this.$router.push('/dashboard');
      } catch (error) {
        console.log(error);
      }
    }
  }
}
</script>
