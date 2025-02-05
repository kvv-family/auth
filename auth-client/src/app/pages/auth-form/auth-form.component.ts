import { Component } from '@angular/core';
import { CardModule } from 'primeng/card';
import { PasswordModule } from 'primeng/password';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import {
  FormBuilder,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
} from '@angular/forms';
import { IftaLabelModule } from 'primeng/iftalabel';
import { ToggleSwitchModule } from 'primeng/toggleswitch';
import { DividerModule } from 'primeng/divider';
import { TooltipModule } from 'primeng/tooltip';

type ServicesTypes = 'vk' | 'yandex';

interface ServiceModel {
  icon: string;
  tooltip: string;
  name: ServicesTypes;
  disabled: boolean;
}

@Component({
  selector: 'app-auth-form',
  imports: [
    CardModule,
    PasswordModule,
    TooltipModule,
    IftaLabelModule,
    InputTextModule,
    ButtonModule,
    FormsModule,
    ReactiveFormsModule,
    ToggleSwitchModule,
    DividerModule,
    FormsModule,
    ReactiveFormsModule,
  ],
  templateUrl: './auth-form.component.html',
  styleUrl: './auth-form.component.scss',
})
export class AuthFormComponent {
  services: ServiceModel[] = [
    {
      icon: 'vk.svg',
      tooltip: 'VK',
      name: 'yandex',
      disabled: true,
    },
    {
      icon: 'yandex.svg',
      tooltip: 'Yandex',
      name: 'vk',
      disabled: true,
    },
  ];

  authForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.authForm = this.fb.group({
      username: [''],
      password: [''],
    });
  }
}
