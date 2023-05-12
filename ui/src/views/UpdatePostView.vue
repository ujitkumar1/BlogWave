<template>
  <div>
    <h2>Update Post</h2>
    <form @submit.prevent="updatePost">
      <div>
        <label for="title">Title</label>
        <input type="text" id="title" v-model="post.title" required>
      </div>
      <div>
        <label for="description">Description</label>
        <textarea id="description" v-model="post.description" required></textarea>
      </div>
      <div>
        <label for="image">Image</label>
        <input type="file" id="image" ref="image" accept="image/*" @change="handleImageUpload">
        <img v-if="post.imageUrl" :src="post.imageUrl" alt="Post Image" width="200px">
      </div>
      <button type="submit">Update Post</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "UpdatePostView",
  data() {
    return {
      post: null,
      imageFile: null,
    };
  },
  created() {
    const postId = this.$route.params.id;
    axios
      .get(`http://localhost:5000/posts/${postId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      })
      .then((response) => {
        this.post = response.data;
      })
      .catch((error) => {
        console.log(error);
      });
  },
  methods: {
    async updatePost() {
      try {
        const formData = new FormData();
        formData.append('title', this.post.title);
        formData.append('description', this.post.description);
        formData.append('image', this.imageFile);
        const response = await axios.put(`http://localhost:5000/posts/${this.post.id}`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
        });
        console.log(response.data);
        this.$router.push('/dashboard');
      } catch (error) {
        console.log(error);
      }
    },
    handleImageUpload() {
      this.imageFile = this.$refs.image.files[0];
      this.post.imageUrl = URL.createObjectURL(this.imageFile);
    },
  },
};
</script>
