import { environment } from '../../../src/environment/environment';

export const API_CONFIG = {
  USER: {
    SIGNUP: `${environment.apiUrl}/user/signup`,
    LOGIN: `${environment.apiUrl}/user/login`,
    RESET_PASSWORD: `${environment.apiUrl}/user/reset-password`,
    PROFILE_PIC: `${environment.apiUrl}/user/profile-pic`,
    ME: `${environment.apiUrl}/user/me`,
    DELETE_PROFILE_PIC: `${environment.apiUrl}/user/profile-pic`
  },
  COMMENTS: {
    BASE: `${environment.apiUrl}/comments`,
    CREATE: `${environment.apiUrl}/comments`,
    GET_ALL: `${environment.apiUrl}/comments`,
    GET_BY_ID: (commentId: string) => `${environment.apiUrl}/comments/${commentId}`,
    UPDATE: (commentId: string) => `${environment.apiUrl}/comments/${commentId}`,
    DELETE: (commentId: string) => `${environment.apiUrl}/comments/${commentId}`,
    LIKE: (commentId: string) => `${environment.apiUrl}/comments/${commentId}/like`,
    REPLIES: (commentId: string) => `${environment.apiUrl}/comments/${commentId}/replies`,
    ADMIN_DELETE: (commentId: string) => `${environment.apiUrl}/comments/admin/${commentId}`
  }
};