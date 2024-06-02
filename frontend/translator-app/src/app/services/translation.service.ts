import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class TranslationService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  translateText(text: string, inputLang: string, outputLang: string): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*' 
    });

    return this.http.post<any>(`${this.apiUrl}/translate`, { text, inputLang, outputLang }, { headers });
  }

  getTextToSpeech(text: string, lang: string): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*' 
    });

    return this.http.post<any>(`${this.apiUrl}/tts`, { text, lang }, { headers });
  }
  
  getLastWords(): Observable<any[]> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*' 
    });

    return this.http.get<any[]>(`${this.apiUrl}/last_words`, { headers });
  }

  saveWord(inputText: string, outputText: string, inputLang: string, outputLang: string): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*' 
    });

    return this.http.post<any>(`${this.apiUrl}/saveword`, { input_text: inputText, output_text: outputText, input_lang: inputLang, output_lang: outputLang}, { headers });
  }

  deleteWord(wordId: number): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    });

    return this.http.delete<any>(`${this.apiUrl}/deleteword/${wordId}`, { headers });
  }
}
