import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../enviroments/environment';

@Injectable({
  providedIn: 'root'
})
export class TranslationService {
  private apiUrl = environment.apiUrl;
  response! : Observable<any> 
  constructor(private http: HttpClient) {}

  translateText(text: string, inputLang: string, outputLang: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/translate`, { text, inputLang, outputLang });
  }

  getTextToSpeech(text: string, lang: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/tts`, { text, lang});
  }
  
  getLastWords(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/last_words`);
  }

  saveWord(inputText: string, outputText: string, inputLang: string, outputLang: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/saveword`, { input_text: inputText, output_text: outputText, input_lang: inputLang, output_lang: outputLang});
  }

  deleteWord(wordId: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/deleteword/${wordId}`);
  }

}
