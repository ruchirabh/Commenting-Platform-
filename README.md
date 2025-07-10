# Angular + Python Comments Application

A full-stack comments application with user authentication, built with:
- **Frontend**: Angular 15+
- **Backend**: Python (FastAPI)
- **Database**: MongoDB
- **Hosting**: 
  - Frontend: Vercel 
  - Backend: Render

## 🔧 What I Learned

- **Angular Fundamentals**: Component architecture, services, and RxJS observables
- **Python Backend Development**: FastAPI framework and MongoDB integration
- **Full-Stack Deployment**: 
  - Hosting Python backends on Render
  - Deploying Angular apps on Vercel
- **Authentication**: JWT handling across frontend and backend
- **Responsive Design**: CSS techniques for mobile-friendly UIs

## 🧗 Hardest Parts

1. **Angular Learning Curve**:
   - Coming from React, Angular's dependency injection and module system required significant adjustment
   - TypeScript strict typing was challenging initially

2. **Responsive Design**:
   - Making the comment threads look good on all devices
   - CSS media query debugging

3. **JWT Implementation**:
   - Proper token storage in frontend
   - Handling token refresh logic
   - Interceptor configuration for API calls

4. **Backend Hosting**:
   - Environment variable configuration on Render
   - CORS setup between frontend and backend

## 🚀 Future Improvements

If given more time, I would:

### Frontend
- [ ] **Improve Component Structure**:
  - Create more reusable presentational components
  - Better separation of UI and business logic
- [ ] **Enhance Design System**:
  - Implement a proper design token system
  - Add dark mode support
- [ ] **Optimize Performance**:
  - Virtual scrolling for long comment threads
  - Better loading states

### Backend
- [ ] **Add Advanced Features**:
  - Comment editing history
  - User mentions (@username)
  - Image uploads in comments
- [ ] **Improve API**:
  - Rate limiting
  - Better error handling

### Infrastructure
- [ ] **CI/CD Pipeline**:
  - Automated testing
  - Staging environment
- [ ] **Monitoring**:
  - Error tracking
  - Performance metrics

## 🛠️ How to Run Locally

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend 
cd frontend
npm install
ng serve
