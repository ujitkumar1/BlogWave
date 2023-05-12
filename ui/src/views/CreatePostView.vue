<template>
  <div>
    <h2>Create Post</h2>
    <form @submit.prevent="createPost">
      <div>
        <label for="title">Title</label>
        <input type="text" id="title" v-model="title" required>
      </div>
      <div>
        <label for="description">Description</label>
        <textarea id="description" v-model="description" required></textarea>
      </div>
      <div>
        <label for="image">Image</label>
        <input type="file" id="image" ref="image" accept="image/*" @change="handleImageUpload" required>
        <img v-if="imageUrl" :src="imageUrl" alt="Post Image" width="200px">
      </div>
      <button type="submit">Create Post</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
console.log("CreatpostView")
export default {
  name: "CreatePostView",
  data() {
    return {
      title: "",
      description: "",
      imageUrl: null,
      imageFile: null,
      userID: sessionStorage.getItem('userID'),
    };
  },
  methods: {
    async createPost() {
      try {
        const formData = new FormData();
        console.log(sessionStorage)
        formData.append('title', this.title);
        formData.append('description', this.description);
        formData.append('image', this.imageFile);
        formData.append('user_id', sessionStorage.getItem("userId"));
        console.log(sessionStorage)
        const response = await axios.post("http://localhost:5000/createposts", formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
        });
        console.log(formData)
        console.log(response.data);
        this.$router.push('/dashboard');
      } catch (error) {
        console.log(error);
      }
    },
    handleImageUpload() {
      this.imageFile = this.$refs.image.files[0];
      this.imageUrl = URL.createObjectURL(this.imageFile);
    },
  },
};
</script>
