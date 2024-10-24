// user.service.ts
import { Injectable } from '@angular/core';

interface User {
  username: string;
  email: string;
  address: string;
  phone: string;
  password: string; // Add password field
}

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private user: User | null = null;

  setUser(user: User) {
    console.log('User set in service:', user); // Debug log
    this.user = user;
  }

  getUser(): User | null {
    console.log('User fetched from service:', this.user); // Debug log
    return this.user;
  }

  validateUser(username: string, password: string): boolean {
    // Check if the stored user matches the provided credentials
    return this.user?.username === username && this.user?.password === password;
  }

  clearUser() {
    console.log('User cleared from service'); // Debug log
    this.user = null;
  }
}
