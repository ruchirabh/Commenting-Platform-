import { Component, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-floating-action-button',
  standalone: true,
  template: `
    <button (click)="toggleForm.emit()"
      class="fixed bottom-6 right-6 bg-amber-100 text-dark p-4 rounded-full shadow-lg hover:bg-indigo-700 transition-all">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
      </svg>
    </button>
  `,
  styles: []
})
export class FloatingActionButtonComponent {
  @Output() toggleForm = new EventEmitter();
}