<template>
  <div>
    <h1>Blog Posts</h1>
    <template v-if="!isLoggedIn">
      <router-link to="/login">Login</router-link> |
      <router-link to="/signup">Signup</router-link>
    </template>
    <template v-else>
      <router-link to="/search">Search Users</router-link> |
      <router-link to="/profile">Profile</router-link> |
      <button v-on:click="logout">Logout</button>
    </template>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  computed: {
    isLoggedIn() {
      // Check if user is logged in by checking if their data is present in sessionStorage
      if (sessionStorage.length == 0) {
        return false;
      }
      else {
        return true;
      }
    }
  },
  methods: {
    logout() {
      // Clear the user data from sessionStorage
      sessionStorage.clear();
      console.log("Method called logout");
      // Navigate back to the root path
      this.$router.push('/');
    }
  }
}
</script>
