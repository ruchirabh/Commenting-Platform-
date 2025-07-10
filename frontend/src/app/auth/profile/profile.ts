import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { Auth } from '../auth';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './profile.html',
  styleUrls: ['./profile.css']
})
export class ProfileComponent implements OnInit {
  profileImage: SafeUrl | string = 'assets/images/default-profile.png';
  userData: any = {
    username: '',
    email: ''
  };
  isLoading = false;
  errorMessage = '';
  successMessage = '';
  selectedFile: File | null = null;

  constructor(
    private authService: Auth,
    private sanitizer: DomSanitizer
  ) {}

  ngOnInit(): void {
    this.loadUserData(); 
    this.loadUserProfile(); 
    this.loadProfilePicture();
  }

  loadUserData(): void {
    const userData = localStorage.getItem('user');
    if (userData) {
      try {
        const user = JSON.parse(userData);
        this.userData.username = user.username || '';
        this.userData.email = user.email || '';
      } catch (e) {
        console.error('Error parsing user data:', e);
      }
    }
  }

  loadUserProfile(): void {
    this.isLoading = true;
    this.authService.getUserProfile().subscribe({
      next: (data) => {
        this.userData = { ...this.userData, ...data };
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Failed to load profile:', err);
        this.isLoading = false;
      }
    });
  }

  loadProfilePicture(): void {
    this.authService.getProfilePicture().subscribe({
      next: (blob) => {
        const objectUrl = URL.createObjectURL(blob);
        this.profileImage = this.sanitizer.bypassSecurityTrustUrl(objectUrl);
      },
      error: () => {
        this.profileImage = 'assets/images/default-profile.png';
      }
    });
  }

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        this.errorMessage = 'File size exceeds 5MB limit';
        return;
      }
      if (!['image/jpeg', 'image/png'].includes(file.type)) {
        this.errorMessage = 'Only JPEG/PNG files are allowed';
        return;
      }
      this.selectedFile = file;
      
      const reader = new FileReader();
      reader.onload = (e: any) => {
        this.profileImage = this.sanitizer.bypassSecurityTrustUrl(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  }

  uploadProfilePicture(): void {
    if (!this.selectedFile) return;

    this.isLoading = true;
    this.errorMessage = '';
    this.successMessage = '';

    this.authService.uploadProfilePicture(this.selectedFile).subscribe({
      next: () => {
        this.successMessage = 'Profile picture updated successfully';
        this.selectedFile = null;
        this.isLoading = false;
        
        this.loadProfilePicture();
      },
      error: (err) => {
        this.errorMessage = err.error?.message || 'Failed to upload profile picture';
        this.isLoading = false;
      }
    });
  }
}