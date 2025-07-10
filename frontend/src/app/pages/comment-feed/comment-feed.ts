import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NavbarComponent } from '../../components/navbar/navbar';
import { CommentListComponent } from '../../components/comment-list/comment-list'; 
import { CommentFormComponent } from '../../components/comment-form/comment-form';
import { CommentService } from '../../components/comment'; 
import { FloatingActionButtonComponent } from '../../components/floating-action-button.component';

@Component({
  selector: 'app-comment-feed',
  standalone: true,
  imports: [
    CommonModule, 
    NavbarComponent, 
    CommentListComponent, 
    CommentFormComponent,
    FloatingActionButtonComponent
  ],
  templateUrl: './comment-feed.html',
  styleUrls: ['./comment-feed.css']
})
export class CommentFeedComponent implements OnInit {
  comments: any[] = [];
  isLoading = true;
  error = '';
  showCommentForm = false;

  constructor(private commentService: CommentService) {}

  ngOnInit(): void {
    this.loadComments();
  }

  loadComments(): void {
    this.isLoading = true;
    this.commentService.getComments().subscribe({
      next: (comments) => {
        this.comments = comments;
        this.isLoading = false;
      },
      error: (err) => {
        this.error = 'Failed to load comments';
        this.isLoading = false;
      }
    });
  }

  toggleCommentForm(): void {
    this.showCommentForm = !this.showCommentForm;
  }

  onCommentAdded(): void {
    this.loadComments();
    this.showCommentForm = false;
  }
}