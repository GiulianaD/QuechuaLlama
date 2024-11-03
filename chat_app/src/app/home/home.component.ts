import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import {MatTabsModule} from '@angular/material/tabs';
import {MatIconModule} from '@angular/material/icon';
import { Message } from '../interfaces/messages';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    FormsModule,
    MatTabsModule,
    MatIconModule
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {
  conversation: Message[] = [];
  userProfile = 'https://i.pinimg.com/550x/f9/e5/90/f9e590368d01c87a14938ecbb96c97ec.jpg';
  assistantProfile = 'https://hips.hearstapps.com/hmg-prod/images/shrek-64f9ceef56099.jpg';

  chatInput: string = '';

  sendMessage() {
    if (this.chatInput.trim()) {
      this.conversation.push({ role: 'user', content: this.chatInput });
      const response = `Echo: ${this.chatInput}`;
      this.conversation.push({ role: 'assistant', content: response });
      this.chatInput = ''; // Clear input
    }
  }

}
