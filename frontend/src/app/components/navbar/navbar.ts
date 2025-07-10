import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Auth } from '../../auth/auth';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';
import { Router } from '@angular/router';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './navbar.html',
  styleUrls: ['./navbar.css']
})
export class NavbarComponent implements OnInit {
  profileImage: SafeUrl | string = 'assets/images/default-profile.png';
  username: string = '';
  email: string = '';

  constructor(
    private authService: Auth,
    private sanitizer: DomSanitizer,
    private router: Router 
  ) {}

  ngOnInit(): void {
    this.loadUserData();
    this.loadProfilePicture();
  }

  loadUserData(): void {
    const userData = localStorage.getItem('user');
    if (userData) {
      try {
        const user = JSON.parse(userData);
        this.username = user.username || '';
        this.email = user.email || '';
      } catch (e) {
        console.error('Error parsing user data:', e);
      }
    }
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

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}