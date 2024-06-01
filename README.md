# T3BE-Transcriptions

This is a machine assisted transcription of T3BE questions from the Opening Arguments Podcast. 

Questions 1-75 were transcribed by a machine from the audio podcast, then cleaned up by hand to contain just the T3BE question text.

Questions 76 onwards were transcribed by Optical Character Recognition from a screenshot of the question (provided to patrons of the podcast at patreon.com/law). And then also manually cleaned up.

The transcriptions may have errors associated with the automation involved. Questions 1-75 are unlikely to have misspellings, but may substitute homophones erroneously. Questions 76 onwards are more likely to have typos that look visually similar (for example, "attomey" rather than "attorney"). Make sure to verify the transcription is accurate before reusing.

"Allquestions.txt" has all the questions texts combined and is probably what you want to view/download. To download, click on the file so it opens in Github's file viewer, then click the "Download raw file" button in the top-right corner of the viewer. If you want a specific question by itself check out the "individualtxtfiles" folder.

If you just want to see questions since the reboot compiled together, look at "RebootQuestions.txt". If you just want to see the old run of questions complied together, look at "OldQuestions.txt"

____

This now also contains a script for tabulating Thomas' T3BE scores and the scores of those who play along with reddit. 

To this end, the answers directory now contains the answers (and guesses), as well as metadata for the questions since the reboot. The results are in lastTenResults.txt and allResults.txt

When there's a new T3BE question, simply add a new file like (for example) "newfile.txt" in the answers directory, fill it out like the others, add a reference to that file in "files" variable at the top of tabulateT3BEResults.py. Then rerun the script with "./runTenAndFull" in a bash terminal. You will need Python3 installed and in your PATH. Then re-view lastTenResults.txt and allResults.txt.

The python script itself works but is a bit of a work in progress in terms of coding standards.

