import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TranslationService {
  private apiUrl = 'http://localhost:5000';
  response! : Observable<any> 
  constructor(private http: HttpClient) {}

  translateText(text: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/translate`, { text });
  }

  getTextToSpeech(text: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/tts`, { text });
  }

}
