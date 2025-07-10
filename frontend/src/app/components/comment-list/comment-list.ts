import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CommentItemComponent } from '../comment-item/comment-item';

@Component({
  selector: 'app-comment-list',
  standalone: true,
  imports: [CommonModule, CommentItemComponent],
  templateUrl: './comment-list.html',
  styleUrls: ['./comment-list.css']
})
export class CommentListComponent {
  @Input() comments: any[] = [];
}