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
  Validators,
} from '@angular/forms';
import { IftaLabelModule } from 'primeng/iftalabel';
import { ToggleSwitchModule } from 'primeng/toggleswitch';
import { DividerModule } from 'primeng/divider';
import { TooltipModule } from 'primeng/tooltip';
import { CadesService } from '../../services/cades.service';
import { InputMaskModule } from 'primeng/inputmask';
import { DatePickerModule } from 'primeng/datepicker';
import {
  trigger,
  state,
  style,
  animate,
  transition,
} from '@angular/animations';
import { AuthService } from '../../services/auth.service';

type ServicesTypes = 'vk' | 'yandex';

type STATES = 'register' | 'auth';

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
    InputMaskModule,
    DatePickerModule,
  ],
  templateUrl: './auth-form.component.html',
  styleUrl: './auth-form.component.scss',
  animations: [
    trigger('registerState', [
      state(
        'register',
        style({
          width: '600px',
          opacity: '1',
        })
      ),
      state(
        'auth',
        style({
          width: '0px',
          opacity: '0',
        })
      ),
      transition('register => auth', [animate('0.2s')]),
      transition('auth => register', [animate('0.2s')]),
    ]),
    trigger('authState', [
      state(
        'register',
        style({
          width: '0px',
          opacity: '0',
        })
      ),
      state(
        'auth',
        style({
          width: '400px',
          opacity: '1',
        })
      ),
      transition('register => auth', [animate('0.2s')]),
      transition('auth => register', [animate('0.2s')]),
    ]),
  ],
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
  registerForm: FormGroup;
  currentState: STATES = 'auth';
  showAuth: boolean = true;
  showRegister: boolean = false;

  constructor(
    private fb: FormBuilder,
    private cades: CadesService,
    private auth: AuthService
  ) {
    this.authForm = this.fb.group({
      username: ['', [Validators.required]],
      password: ['', [Validators.required]],
      remeber: [false],
    });
    this.registerForm = this.fb.group({
      username: ['', [Validators.required]],
      password: ['', [Validators.required, Validators.min(6)]],
      replyPassword: ['', [Validators.required]],
      phone: ['', [Validators.required]],
      email: ['', [Validators.required]],
      firstname: ['', [Validators.required]],
      lastname: ['', [Validators.required]],
      middlename: [''],
      datebirth: ['', [Validators.required]],
    });
  }

  submitAuth() {
    console.log('SUBMIT', this.authForm.valid);
    if (this.authForm.valid) {
      const values = this.authForm.value;
      this.auth.authorizeLocale(values.username, values.password);
    }
  }

  changeState(state: STATES) {
    this.currentState = state;
  }

  startAnimation() {
    if (this.currentState == 'auth') {
      this.showAuth = true;
    } else {
      this.showRegister = true;
    }
  }

  doneAnimation() {
    if (this.currentState == 'auth') {
      this.showAuth = true;
      this.showRegister = false;
    } else {
      this.showAuth = false;
      this.showRegister = true;
    }
  }
}
