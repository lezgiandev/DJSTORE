import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/tracks',
      name: 'tracks',
      component: () => import('../views/TracksView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/tracks/add',
      name: 'add-track',
      component: () => import('../views/TrackAddView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/tracks/:id/edit',
      name: 'edit-track',
      component: () => import('../views/TrackEditView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/requests',
      name: 'requests',
      component: () => import('../views/RequestsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/finance',
      name: 'finance',
      component: () => import('../views/FinanceView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/withdrawals',
      name: 'withdrawals',
      component: () => import('../views/WithdrawalsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/venue/:id/request',
      name: 'venue-request',
      component: () => import('../views/VenueRequestView.vue')
    },
    {
      path: '/request/pay/:token',
      name: 'request-payment',
      component: () => import('../views/RequestPaymentView.vue')
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue')
    }
  ]
});

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const isAuthenticated = !!localStorage.getItem('access_token');

  if (requiresAuth && !isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});

export default router; 