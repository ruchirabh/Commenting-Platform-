import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CommentService } from '../comment';

@Component({
  selector: 'app-comment-form',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './comment-form.html',
  styleUrls: ['./comment-form.css'],
})
export class CommentFormComponent {
  @Input() placeholder: string = 'Write a comment...';
  @Input() parentId?: string;
  @Output() commentAdded = new EventEmitter<void>();
  
  showForm = true; // Add this line to control visibility

  content = '';
  isLoading = false;
  error = '';

  constructor(private commentService: CommentService) {}

  submitComment(): void {
    if (!this.content.trim()) {
      this.error = 'Comment cannot be empty';
      return;
    }

    this.isLoading = true;
    this.error = '';

    this.commentService.createComment(this.content, this.parentId).subscribe({
      next: () => {
        this.content = '';
        this.isLoading = false;
        this.commentAdded.emit();
        this.showForm = false; // Hide after successful submission
      },
      error: (err) => {
        this.error = err.error?.message || 'Failed to post comment';
        this.isLoading = false;
      },
    });
  }

  cancel(): void {
    this.showForm = false; // Hide the form when cancelled
    this.content = '';
    this.error = '';
  }
}