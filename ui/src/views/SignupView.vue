<template>
  <div>
    <h1>Signup</h1>
    <form @submit.prevent="signup">
      <div>
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="name">
      </div>
        <div>
        <label for="email">Email:</label>
        <input type="text" id="email" v-model="email">
      </div>
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username">
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password">
      </div>
      <div>
        <button type="submit">Signup</button>
      </div>
    </form>
  </div>
</template>
<script>
import axios from 'axios'

export default {
  name: 'SignupView',
  data() {
    return {
      name: '',
      username: '',
      password: '',
        email: ''
    }
  },
  methods: {
    async signup() {
      try {
        const response = await axios.post('http://localhost:5000/signup', {
          name: this.name,
          username: this.username,
          password: this.password,
            email: this.email

        });

        console.log(response.data);

        const userResponse = await axios.get(`http://localhost:5000/users?username=${this.username}`, {
          headers: {
            'Authorization': `Bearer ${response.data.token}`,
          },
        });

        const userId = userResponse.data.id;

        sessionStorage.setItem("userId", userId);


        sessionStorage.setItem("username", this.username);
        sessionStorage.setItem("password", this.password);
        sessionStorage.setItem("name", this.name);


        this.$router.push('/dashboard');
      } catch (error) {
        console.log(error)
      }
    }
  }
}
</script>
