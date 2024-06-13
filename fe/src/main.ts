import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
// import VueGoogleMaps from '@fawmi/vue-google-maps'
import VueGoogleMaps from 'vue-google-maps-community-fork'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(VueGoogleMaps, {
  load: {
    key: import.meta.env.VITE_GOOGLE_MAPS_API_KEY
  }
})

app.mount('#app')
