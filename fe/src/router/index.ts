import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RaceView from '../views/RaceView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/race/:raceId',
      name: 'race',
      component: RaceView,
      props: true // Pass route params as props to the component
    }
  ]
})

export default router
