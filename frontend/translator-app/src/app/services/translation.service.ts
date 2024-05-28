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

  translateText(text: string, inputLang: string, outputLang: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/translate`, { text, inputLang, outputLang });
  }

  getTextToSpeech(text: string, inputLang: string, outputLang: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/tts`, { text, inputLang, outputLang});
  }
  
  getLastWords(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/last_words`);
  }

  saveWord(englishText: string, translatedText: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/saveword`, { english_text: englishText, translated_text: translatedText });
  }

}
