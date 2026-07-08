import { createRouter, createWebHistory } from 'vue-router'
import HomeView from "@/views/home/HomeView.vue";
import LoginView from "@/views/user/LoginView.vue";
import RegisterView from "@/views/user/RegisterView.vue";
import ResearchView from "@/views/chat/ResearchView.vue";
import ProjectsView from "@/views/project/ProjectsView.vue";
import ReportView from "@/views/report/ReportView.vue";
import ResetPwdView from "@/views/user/ResetPwdView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home-index',
      component: HomeView
    },
    {
      path: '/user/login',
      name: 'user-login-index',
      component: LoginView
    },
    {
      path: '/user/register',
      name: 'user-register-index',
      component: RegisterView
    },
    {
      path: '/user/resetpwd',
      name: 'user-resetpwd-index',
      component: ResetPwdView
    },
    {
      path: '/chat',
      name: 'chat-index',
      component: ResearchView
    },
    {
      path: '/project',
      name: 'project-index',
      component: ProjectsView
    },
    {
      path: '/report',
      name: 'report-index',
      component: ReportView
    },
  ],
})

export default router
