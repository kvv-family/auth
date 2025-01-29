import { Component } from '@angular/core';
import { CardModule } from 'primeng/card';
import { PasswordModule } from 'primeng/password';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { IftaLabelModule } from 'primeng/iftalabel';
import { ToggleSwitchModule } from 'primeng/toggleswitch';

@Component({
  selector: 'app-root',
  imports: [CardModule, PasswordModule, IftaLabelModule, InputTextModule, ButtonModule, FormsModule, ReactiveFormsModule, ToggleSwitchModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'auth-client';
}
