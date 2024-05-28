import { Component, Injector } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { TranslationService } from '../services/translation.service';


@Component({
  selector: 'app-main',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './main.component.html',
  styleUrl: './main.component.scss'
})
export class MainComponent {
  inputText: string = '';
  translatedText: string = '';
  audioUrl: string = '';

  constructor(private translationService: TranslationService) {}


  translateText(): void {
    this.translationService.translateText(this.inputText).subscribe(
      (response) => {
        this.translatedText = response.translated_text;
      },
      (error) => {
        console.error('Error:', error);
      }
    );
  }

  getTextToSpeech(text: string): void {
    this.translationService.getTextToSpeech(text).subscribe(
      (response) => {
        // Add a cache-busting parameter to the audio URL
        const cacheBuster = new Date().getTime();
        this.audioUrl = `http://localhost:5000/get_tts?filename=${response.tts_filename}&cb=${cacheBuster}`;
        this.playAudio(this.audioUrl);
      },
      (error) => {
        console.error('Error:', error);
      }
    );
  }

  playAudio(url: string): void {
    const audio = new Audio(url);
    audio.play();
  }
  
}
