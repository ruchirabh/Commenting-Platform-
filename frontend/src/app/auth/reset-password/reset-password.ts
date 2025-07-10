import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormsModule,
  ReactiveFormsModule,
  FormBuilder,
  FormGroup,
  Validators,
  AbstractControl,
} from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { Auth } from '../auth';

@Component({
  selector: 'app-reset-password',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, RouterModule],
  templateUrl: './reset-password.html',
  styleUrls: ['./reset-password.css'],
})
export class ResetPasswordComponent implements OnInit {
  resetForm: FormGroup;
  errorMessage: string = '';
  successMessage: string = '';
  isLoading: boolean = false;

  constructor(
    private fb: FormBuilder,
    private authService: Auth,
    private router: Router
  ) {
    this.resetForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      new_password: [
        '',
        [
          Validators.required,
          Validators.minLength(8),
          this.strongPasswordValidator,
        ],
      ],
    });
  }

  ngOnInit() {
    window.history.pushState(null, '', window.location.href);
    window.addEventListener('popstate', () => {
      window.history.pushState(null, '', window.location.href);
    });
  }

  strongPasswordValidator(control: AbstractControl) {
    const value = control.value || '';
    const strongPasswordRegex =
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?#&^()_+=-])[A-Za-z\d@$!%*?#&^()_+=-]{8,}$/;
    return strongPasswordRegex.test(value) ? null : { weakPassword: true };
  }

  onSubmit() {
    this.errorMessage = '';
    this.successMessage = '';

    if (this.resetForm.invalid) {
      return;
    }

    this.isLoading = true;
    const { email, new_password } = this.resetForm.value;
    const payload = { email, new_password };

    this.authService.resetPassword(payload).subscribe({
      next: (response) => {
        this.successMessage = response.message || 'Password reset successful! Redirecting to login...';
        
        window.removeEventListener('popstate', () => {});

        setTimeout(() => {
          this.router.navigate(['/login'], { 
            replaceUrl: true 
          }).then(() => {
            window.history.pushState(null, '', window.location.href);
          });
        }, 2000);
      },
      error: (error) => {
        this.errorMessage = error.error?.message || 'Password reset failed. Please try again.';
        console.error('Reset password error:', error);
        this.isLoading = false;
      }
    });
  }

  get email() {
    return this.resetForm.get('email');
  }

  get new_password() {
    return this.resetForm.get('new_password');
  }
}