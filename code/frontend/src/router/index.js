import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterPage from '../views/RegisterPage.vue'
import LoginPage from '../views/LoginPage.vue'
import CreateSection from '../views/CreateSection.vue'
import AllSections from '../views/AllSections.vue'
import AddBooks from '../views/AddBooks.vue'
import AllBooks from '../views/AllBooks.vue'
import UpdateBook from '../views/UpdateBook.vue'
import ViewBook from '../views/ViewBook.vue'
import UpdateSection from '../views/UpdateSection.vue'
import RequestedBooks from '@/views/RequestedBooks.vue';
import  UserRequests from '@/views/UserRequests.vue';
import UserStat from '@/views/UserStat.vue';
import WaitBook from '@/views/WaitBook.vue';
import AdminStat from '@/views/AdminStat.vue';
import MyBooks from '@/views/MyBooks.vue';
import SubmitFeedback from '@/views/SubmitFeedback.vue';
import MyFeedbacks from '@/views/MyFeedbacks.vue';
import AdminFeedback from '@/views/AdminFeedback.vue';
import GraphStats from '@/views/GraphStats.vue';
import MyProfile from '@/views/MyProfile.vue';
import UpdateProfile from '@/views/UpdateProfile.vue';
import AllUsers from '@/views/AllUsers.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },

  {
    path: '/register',
    name: 'register',
    component: RegisterPage
  },
  
  {
    path: '/login',
    name: 'login',
    component: LoginPage
  },

  {
    path: '/createsection',
    name: 'createsection',
    component: CreateSection
  },

  {
    path: '/allsections',
    name: 'allsections',
    component: AllSections
  },

  {
    path: '/allbooks',
    name: 'allbooks',
    component: AllBooks
  },

  {
    path: '/add-books/:id',
    name: 'addbooks',
    component: AddBooks
  },

  {
    path: '/update-book/:id',
    name: 'updatebook',
    component: UpdateBook
  },

  {
    path: '/view-book/:id',
    name: 'viewbook',
    component: ViewBook
  },

  {
    path: '/requested-books',
    name: 'requestedbooks',
    component: RequestedBooks,
  },

  {
    path: '/user-requests',
    name: 'userrequests',
    component: UserRequests,
  },

  {
    path: '/wait-book/:bookId',
    name: 'waitbook',
    component: WaitBook
  },

  {
    path: '/user-stat',
    name: 'userstat',
    component: UserStat,
  },

  {
    path: '/admin-stats',
    name: 'adminstat',
    component: AdminStat,
  },

  {
    path: '/mybooks',
    name: 'mybooks',
    component: MyBooks
  },
  
  {
    path: '/update-section/:id',
    name: 'updatesection',
    component: UpdateSection
  },

  {
    path: '/submit-feedback',
    name: 'submitfeedback',
    component: SubmitFeedback
  },

  {
    path: '/my-feedbacks',
    name: 'myfeedbacks',
    component: MyFeedbacks
  },

  {
    path: '/admin-feedback',
    name: 'adminfeedback',
    component: AdminFeedback
  },

  {
    path: '/graph-stats',
    name: 'graphstats',
    component: GraphStats
  },

  {
    path: '/my-profile',
    name: 'myprofile',
    component: MyProfile
  },

  {
    path: '/update-profile',
    name: 'updateprofile',
    component: UpdateProfile
  },

  {
    path: '/all-users',
    name: 'allusers',
    component: AllUsers
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
