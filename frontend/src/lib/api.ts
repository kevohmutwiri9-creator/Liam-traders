import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  login: (email: string, password: string) =>
    api.post('/auth/jwt/create/', { email, password }),
  register: (data: any) =>
    api.post('/auth/users/', data),
  logout: () =>
    api.post('/auth/jwt/blacklist/', { refresh: localStorage.getItem('refresh_token') }),
  forgotPassword: (data: { email:string }) =>
    api.post('/auth/users/reset_password/', data),
  me: () =>
    api.get('/users/profile/'),
};

// User API
export const userAPI = {
  getProfile: () =>
    api.get('/users/profile/'),
  updateProfile: (data: any) =>
    api.patch('/users/profile/', data),
  changePassword: (data: any) =>
    api.post('/auth/users/set_password/', data),
  getSkills: () =>
    api.get('/users/skills/'),
  createSkill: (data: any) =>
    api.post('/users/skills/', data),
  getLevelRequirements: () =>
    api.get('/users/level-requirements/'),
  upgradeLevel: () =>
    api.post('/users/upgrade-level/'),
  getNotifications: () =>
    api.get('/users/notifications/'),
  markNotificationAsRead: (id: number) =>
    api.patch(`/users/notifications/${id}/`, { is_read: true }),
  markAllNotificationsAsRead: () =>
    api.post('/users/notifications/mark-all-read/'),
  getReferralLeaderboard: (limit?: number) =>
    api.get('/users/referral/leaderboard/', { params: { limit } }),
  getReferralHistory: () =>
    api.get('/users/referral/history/'),
  getReferralStats: () =>
    api.get('/users/referral/stats/'),
};

// Tasks API
export const tasksAPI = {
  getTasks: (params?: any) =>
    api.get('/tasks/', { params }),
  getTask: (id: number) =>
    api.get(`/tasks/${id}/`),
  createTask: (data: any) =>
    api.post('/tasks/', data),
  getMyTasks: () =>
    api.get('/tasks/my-tasks/'),
  getAssignedTasks: () =>
    api.get('/tasks/assigned/'),
  applyToTask: (taskId: number, data: any) =>
    api.post(`/tasks/${taskId}/applications/`, data),
  getMyApplications: () =>
    api.get('/tasks/applications/my/'),
  submitTask: (taskId: number, data: any) =>
    api.post(`/tasks/${taskId}/submissions/`, data),
  getMySubmissions: () =>
    api.get('/tasks/submissions/my/'),
  getStatistics: () =>
    api.get('/tasks/statistics/'),
};

// Surveys API
export const surveysAPI = {
  getSurveys: (params?: any) =>
    api.get('/surveys/', { params }),
  getSurvey: (id: number) =>
    api.get(`/surveys/${id}/`),
  getSurveyQuestions: (surveyId: number) =>
    api.get(`/surveys/${surveyId}/questions/`),
  submitSurvey: (surveyId: number, data: any) =>
    api.post(`/surveys/${surveyId}/submit/`, data),
  getMyResponses: () =>
    api.get('/surveys/my-responses/'),
  getStatistics: () =>
    api.get('/surveys/statistics/'),
};

// Courses API
export const coursesAPI = {
  getCourses: (params?: any) =>
    api.get('/courses/', { params }),
  getCourse: (id: number) =>
    api.get(`/courses/${id}/`),
  getMyCourses: () =>
    api.get('/courses/my-courses/'),
  enrollInCourse: (courseId: number) =>
    api.post('/courses/enrollments/', { course_id: courseId }),
  getMyEnrollments: () =>
    api.get('/courses/enrollments/'),
  getCourseLessons: (courseId: number) =>
    api.get(`/courses/${courseId}/lessons/`),
  updateProgress: (enrollmentId: number, data: any) =>
    api.post(`/courses/enrollments/${enrollmentId}/progress/`, data),
  getCourseReviews: (courseId: number) =>
    api.get(`/courses/${courseId}/reviews/`),
  addReview: (courseId: number, data: any) =>
    api.post(`/courses/${courseId}/reviews/`, data),
  getStatistics: () =>
    api.get('/courses/statistics/'),
};

// Wallet API
export const walletAPI = {
  getWallet: () =>
    api.get('/wallet/'),
  getTransactions: (params?: any) =>
    api.get('/wallet/transactions/', { params }),
  getWithdrawals: () =>
    api.get('/wallet/withdrawals/'),
  createWithdrawal: (data: any) =>
    api.post('/wallet/withdrawals/', data),
  getEarnings: (params?: any) =>
    api.get('/wallet/earnings/', { params }),
  getStatistics: () =>
    api.get('/wallet/statistics/'),
};

// Payments API
export const paymentsAPI = {
  initiateWithdrawal: (data: any) =>
    api.post('/payments/mpesa/withdraw/', data),
  getPaymentMethods: () =>
    api.get('/payments/methods/'),
  addPaymentMethod: (data: any) =>
    api.post('/payments/methods/', data),
  // Level upgrade payments
  submitLevelPayment: (data: any) =>
    api.post('/users/payments/', data),
  getMyPayments: () =>
    api.get('/users/payments/'),
  getPendingPayments: () =>
    api.get('/users/payments/pending/'),
  approvePayment: (paymentId: number, data: any) =>
    api.patch(`/users/payments/${paymentId}/approve/`, data),
};

export default api;
