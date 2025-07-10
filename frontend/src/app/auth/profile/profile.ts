// profile.component.ts
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
  userData: any = {};
  isLoading = false;
  errorMessage = '';
  successMessage = '';
  selectedFile: File | null = null;

  constructor(
    private authService: Auth,
    private sanitizer: DomSanitizer
  ) {}

  ngOnInit(): void {
    this.loadUserProfile();
  }

  loadUserProfile(): void {
    this.isLoading = true;
    this.authService.getUserProfile().subscribe({
      next: (data) => {
        this.userData = data;
        this.loadProfilePicture();
      },
      error: (err) => {
        this.errorMessage = 'Failed to load profile data';
        console.error(err);
        this.isLoading = false;
      }
    });
  }

  loadProfilePicture(): void {
    this.authService.getProfilePicture().subscribe({
      next: (blob) => {
        const objectUrl = URL.createObjectURL(blob);
        this.profileImage = this.sanitizer.bypassSecurityTrustUrl(objectUrl);
        this.isLoading = false;
      },
      error: () => {
        this.profileImage = 'assets/images/default-profile.png';
        this.isLoading = false;
      }
    });
  }

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) { // 5MB limit
        this.errorMessage = 'File size exceeds 5MB limit';
        return;
      }
      if (!['image/jpeg', 'image/png'].includes(file.type)) {
        this.errorMessage = 'Only JPEG/PNG files are allowed';
        return;
      }
      this.selectedFile = file;
      
      // Preview the image
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
      },
      error: (err) => {
        this.errorMessage = err.error?.message || 'Failed to upload profile picture';
        this.isLoading = false;
      }
    });
  }
}