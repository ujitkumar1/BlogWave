import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios';

Vue.config.productionTip = false
axios.defaults.headers.common['Content-Type'] = 'application/json';
new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
