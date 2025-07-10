import { Component, Input, OnInit, OnDestroy, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Auth } from '../../auth/auth';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';
import { CommentService } from '../comment';
import { CommentFormComponent } from '../comment-form/comment-form';

@Component({
  selector: 'app-comment-item',
  standalone: true,
  imports: [CommonModule, CommentFormComponent],
  templateUrl: './comment-item.html',
  styleUrls: ['./comment-item.css'],
})
export class CommentItemComponent implements OnInit, OnDestroy {
  @Input() comment: any;
  @Output() commentDeleted = new EventEmitter<number>();
  @Input() placeholder: string = 'Write a comment...'; 
  @Output() commentUpdated = new EventEmitter<any>();
  
  profileImage: SafeUrl | string = 'assets/images/default-profile.png';
  showReplyForm = false;
  isLiked = false;
  isUsersComment = false;
  showReplies = false;
  replies: any[] = [];
  loadingReplies = false;
  likeAnimation = false;
  isLiking = false;
  
  // Keep track of created blob URLs for cleanup
  private blobUrls: string[] = [];

  constructor(
    private authService: Auth,
    private commentService: CommentService,
    private sanitizer: DomSanitizer
  ) {}

  ngOnInit(): void {
    this.loadProfilePicture();
    this.checkIfLiked();
    this.checkIfUsersComment();
  }

  ngOnDestroy(): void {
    // Clean up blob URLs to prevent memory leaks
    this.blobUrls.forEach(url => {
      URL.revokeObjectURL(url);
    });
  }

  loadProfilePicture(): void {
    this.authService.getProfilePicture(this.comment.author_id).subscribe({
      next: (blob) => {
        // Check if the blob is actually an image and has content
        if (blob && blob.size > 0 && blob.type.startsWith('image/')) {
          const objectUrl = URL.createObjectURL(blob);
          this.blobUrls.push(objectUrl); // Track for cleanup
          this.profileImage = this.sanitizer.bypassSecurityTrustUrl(objectUrl);
        } else {
          console.warn('Invalid or empty image blob received');
          this.setDefaultProfileImage();
        }
      },
      error: (err) => {
        console.warn('Failed to load profile picture, using default:', err.message || err);
        this.setDefaultProfileImage();
      }
    });
  }

  private setDefaultProfileImage(): void {
    // Try multiple possible paths for the default image
    const defaultPaths = [
      'assets/images/default-profile.png',
      'assets/default-profile.png',
      'assets/images/default-avatar.png',
      'assets/default-avatar.png'
    ];
    
    // Use the first path as default, but you might want to implement
    // a mechanism to test which path actually exists
    this.profileImage = defaultPaths[0];
    
    // Optional: Test if the image exists
    this.testImagePath(defaultPaths[0]).then(exists => {
      if (!exists) {
        // Try other paths or use a data URL as fallback
        this.profileImage = this.generateDefaultAvatar();
      }
    });
  }

  private testImagePath(path: string): Promise<boolean> {
    return new Promise((resolve) => {
      const img = new Image();
      img.onload = () => resolve(true);
      img.onerror = () => resolve(false);
      img.src = path;
    });
  }

  private generateDefaultAvatar(): string {
    // Generate a simple SVG avatar as fallback
    const initial = (this.comment.username || 'U').charAt(0).toUpperCase();
    const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'];
    const color = colors[this.comment.author_id % colors.length];
    
    const svg = `
      <svg width="40" height="40" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
        <circle cx="20" cy="20" r="20" fill="${color}"/>
        <text x="20" y="25" font-family="Arial, sans-serif" font-size="16" font-weight="bold" 
              text-anchor="middle" fill="white">${initial}</text>
      </svg>
    `;
    
    return `data:image/svg+xml;base64,${btoa(svg)}`;
  }

  checkIfLiked(): void {
    const currentUser = this.authService.getCurrentUser();
    if (currentUser && this.comment.likes) {
      this.isLiked = this.comment.likes.includes(currentUser.user_id);
    }
  }

 checkIfUsersComment(): void {
  const currentUser = this.authService.getCurrentUser();
  const authorId = this.comment.author_id || this.comment.authorId || this.comment.user_id;

  console.log('Current User ID:', currentUser?.user_id);
  console.log('Comment Author ID:', authorId);

  if (currentUser) {
    this.isUsersComment = authorId === currentUser.user_id;
    console.log('Is User\'s Comment?', this.isUsersComment);
  }
}


  toggleLike(): void {
    if (this.isLiking) return; // Prevent multiple clicks
    
    this.isLiking = true;
    this.likeAnimation = true;
    
    // Optimistic update
    const wasLiked = this.isLiked;
    this.isLiked = !wasLiked;
    
    // Update like count optimistically
    if (!this.comment.likes) {
      this.comment.likes = [];
    }
    
    const currentUser = this.authService.getCurrentUser();
    if (currentUser) {
      if (wasLiked) {
        // Remove like
        this.comment.likes = this.comment.likes.filter((id: string) => id !== currentUser.user_id);
      } else {
        // Add like
        this.comment.likes.push(currentUser.user_id);
      }
    }
    
    this.commentService.likeComment(this.comment.id).subscribe({
      next: (updatedComment) => {
        // Update with server response
        this.comment = updatedComment;
        this.checkIfLiked();
        this.isLiking = false;
        
        // Stop animation after a delay
        setTimeout(() => {
          this.likeAnimation = false;
        }, 600);
        
        // Emit update to parent
        this.commentUpdated.emit(updatedComment);
      },
      error: (err) => {
        console.error('Error liking comment:', err);
        // Revert optimistic update
        this.isLiked = wasLiked;
        if (currentUser) {
          if (wasLiked) {
            this.comment.likes.push(currentUser.user_id);
          } else {
            this.comment.likes = this.comment.likes.filter((id: string) => id !== currentUser.user_id);
          }
        }
        this.isLiking = false;
        this.likeAnimation = false;
      },
    });
  }

  toggleReplyForm(): void {
    this.showReplyForm = !this.showReplyForm;
    
    // Auto-focus on reply form when opened
    if (this.showReplyForm) {
      setTimeout(() => {
        const textarea = document.querySelector('.reply-form textarea') as HTMLTextAreaElement;
        if (textarea) {
          textarea.focus();
        }
      }, 100);
    }
  }

  deleteComment(): void {
    const confirmMessage = 'Are you sure you want to delete this comment? This action cannot be undone.';
    
    if (confirm(confirmMessage)) {
      this.commentService.deleteComment(this.comment.id).subscribe({
        next: () => {
          // Emit to parent component to handle removal
          this.commentDeleted.emit(this.comment.id);
          
          // Show success message (you can implement toast notifications)
          console.log('Comment deleted successfully');
        },
        error: (err) => {
          console.error('Error deleting comment:', err);
          alert('Failed to delete comment. Please try again.');
        },
      });
    }
  }

  toggleReplies(): void {
    this.showReplies = !this.showReplies;
    
    if (this.showReplies && this.replies.length === 0) {
      this.loadReplies();
    }
  }

  loadReplies(): void {
    this.loadingReplies = true;
    
    this.commentService.getReplies(this.comment.id).subscribe({
      next: (replies) => {
        this.replies = replies;
        this.loadingReplies = false;
        
        // Update reply count
        this.comment.reply_count = replies.length;
      },
      error: (err) => {
        console.error('Error loading replies:', err);
        this.loadingReplies = false;
      },
    });
  }

  onReplyAdded(): void {
    // Refresh replies and increment count
    this.loadReplies();
    this.showReplyForm = false;
    
    // Increment reply count optimistically
    this.comment.reply_count = (this.comment.reply_count || 0) + 1;
    
    // Emit update to parent
    this.commentUpdated.emit(this.comment);
  }

  onReplyDeleted(replyId: number): void {
    // Remove reply from local array
    this.replies = this.replies.filter(reply => reply.id !== replyId);
    
    // Update reply count
    this.comment.reply_count = Math.max(0, (this.comment.reply_count || 0) - 1);
    
    // Emit update to parent
    this.commentUpdated.emit(this.comment);
  }

  onReplyUpdated(updatedReply: any): void {
    // Update reply in local array
    const index = this.replies.findIndex(reply => reply.id === updatedReply.id);
    if (index !== -1) {
      this.replies[index] = updatedReply;
    }
  }

  // Utility method to format time ago
  getTimeAgo(date: string): string {
    const now = new Date();
    const commentDate = new Date(date);
    const diffMs = now.getTime() - commentDate.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    
    return commentDate.toLocaleDateString();
  }

  // Method to handle keyboard interactions
  onKeydown(event: KeyboardEvent, action: string): void {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      
      switch (action) {
        case 'like':
          this.toggleLike();
          break;
        case 'reply':
          this.toggleReplyForm();
          break;
        case 'toggleReplies':
          this.toggleReplies();
          break;
        case 'delete':
          this.deleteComment();
          break;
      }
    }
  }
}