import { Component} from '@angular/core';
import { FormsModule } from '@angular/forms';
import { TranslationService } from '../services/translation.service';
import { CommonModule } from '@angular/common';
import { Language, LanguageNames } from '../enums/language.enum';


@Component({
  selector: 'app-main',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './main.component.html',
  styleUrl: './main.component.scss'
})
export class MainComponent {
  inputText: string = '';
  outputText: string = '';
  audioUrl: string = '';
  savedWords: any[] = [];
  copySuccess: boolean = false; // Flag to show copy success message
  selectedInputLanguage: Language = Language.English; // Default language code for English
  selectedOutputLanguage: Language = Language.Japanese; 
  languages = Object.keys(Language) as Language[]; 
  languageNames = LanguageNames;

  constructor(private translationService: TranslationService) {}

  ngOnInit(): void {
    this.getLastWords();
    console.log(Language.Japanese)
  }

  getLanguageCode(lang: string): Language {
    return (Language as any)[lang];
  }

  getLanguageName(languageCode: Language): string {
    return LanguageNames[languageCode];
  }


  translateText(): void {
    if (!this.inputText.trim()) {
      this.outputText = ''; // Clear the translated text if input is empty
      return; // Exit the method without making the API call
    }

    this.translationService.translateText(this.inputText, this.selectedInputLanguage, this.selectedOutputLanguage).subscribe(
      (response) => {
        this.outputText = response.translated_text;
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
      this.outputText = '';
    }
  }

  getTextToSpeech(text: string): void {
    this.translationService.getTextToSpeech(text, this.selectedInputLanguage, this.selectedOutputLanguage).subscribe(
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

  saveText(inputText: string, outputText: string, inputLang: string, outputLang:string ): void {
    this.translationService.saveWord(inputText, outputText, inputLang, outputLang).subscribe(
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
    this.inputText = word.input_text;
    this.outputText = word.output_text;
    console.log(word.input_lang)
    this.selectedInputLanguage = this.getLanguageCode(word.input_lang);
    this.selectedOutputLanguage = this.getLanguageCode(word.output_lang);
    // Optionally, trigger the translation again if needed
    this.translateText();
  }

  copyText(): void {
    const textArea = document.createElement('textarea');
    textArea.value = this.outputText;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand('copy');
    document.body.removeChild(textArea);
    this.copySuccess = true;
    setTimeout(() => {
      this.copySuccess = false;
    }, 2000); // Message will disappear after 2 seconds
  }
  
}
