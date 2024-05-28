import { Component} from '@angular/core';
import { FormsModule } from '@angular/forms';
import { TranslationService } from '../services/translation.service';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-main',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './main.component.html',
  styleUrl: './main.component.scss'
})
export class MainComponent {
  inputText: string = '';
  translatedText: string = '';
  audioUrl: string = '';
  savedWords: any[] = [];
  selectedInputLanguage: string = 'en';
  selectedTargetLanguage: string = 'ja'; // Default language code for Japanese
  languages: { name: string, code: string }[] = [
    { name: 'English', code: 'en' },
    { name: 'Japanese', code: 'ja' },
    { name: 'Spanish', code: 'es' },
    { name: 'French', code: 'fr' },
    { name: 'German', code: 'de' },
    // Add more languages as needed
  ];

  constructor(private translationService: TranslationService) {}

  ngOnInit(): void {
    this.getLastWords();
  }


  translateText(): void {
    if (!this.inputText.trim()) {
      this.translatedText = ''; // Clear the translated text if input is empty
      return; // Exit the method without making the API call
    }

    this.translationService.translateText(this.inputText, this.selectedInputLanguage, this.selectedTargetLanguage).subscribe(
      (response) => {
        this.translatedText = response.translated_text;
      },
      (error) => {
        console.error('Error:', error);
      }
    );
  }
  
  clearTextAreas(newText: string): void {
    // Clear both input and translated text areas if the new text is empty
    if (!newText.trim()) {
      this.inputText = '';
      this.translatedText = '';
    }
  }

  getTextToSpeech(text: string): void {
    this.translationService.getTextToSpeech(text, this.selectedInputLanguage, this.selectedTargetLanguage).subscribe(
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

  getLastWords(): void {
    this.translationService.getLastWords().subscribe(
      (response) => {
        this.savedWords = response;
      },
      (error) => {
        console.error('Error fetching last words:', error);
      }
    );
  }

  saveText(englishText: string, translatedText: string): void {
    this.translationService.saveWord(englishText, translatedText).subscribe(
      (response) => {
        console.log('Text saved successfully:', response);
        // Optionally, you can update the list of saved words here
        this.getLastWords();
      },
      (error) => {
        console.error('Error saving text:', error);
      }
    );
  }
  onSavedWordClick(word: any): void {
    this.inputText = word.english_text;
    this.translatedText = word.translated_text;
    // Optionally, trigger the translation again if needed
    this.translateText();
  }
  
}
