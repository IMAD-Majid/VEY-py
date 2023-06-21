"""
PROJECT NAME : VEY
VERSION      : 2.0
CREATOR      : Imad Majid
"""

# SPEED READER
# IMAGES
# FLASHCARDS

import tkinter as tk
from tkinter import filedialog
import pickle as pckl
from copy import deepcopy
from random import choice as randchoice

#       Warning     Text    Button    LightBG     BG
colors=("#f82241", "#fff", "#d7dc2e", "#4d4d4d", "#1d1d1d")

class F(tk.Frame):
    def __init__(self, master, **kwargs):
        if "bg" not in kwargs:
            kwargs["bg"]=colors[4]

        super().__init__(master, **kwargs)

class L(tk.Label):
    def __init__(self, master, text='', **kwargs):
        if "fg" not in kwargs:
            kwargs["fg"]=colors[1]
        if "bg" not in kwargs:
            kwargs["bg"]=colors[4]
        if "font" not in kwargs:
            kwargs["font"]=app.font
        super().__init__(master, text=text,**kwargs)

class B(tk.Button):
    def __init__(self, master, text, **kwargs):
        if "bg" not in kwargs:
            kwargs["bg"]=colors[2]
        if "font" not in kwargs:
            kwargs["font"]=app.font
        if "relief" not in kwargs:
            kwargs["relief"]="flat"
        super().__init__(master, text=text,**kwargs)
    def pack(self, **kwargs):
        if "padx" not in kwargs:
            kwargs["padx"]=1
        if "pady" not in kwargs:
            kwargs["pady"]=1
        super().pack(**kwargs)

class C(tk.Checkbutton):
    def __init__(self, master, text, **kwargs):
        if "bg" not in kwargs:
            kwargs["bg"]=colors[3]
        if "font" not in kwargs:
            kwargs["font"]=app.font

        kwargs["anchor"]="w"
        super().__init__(master, text=text,**kwargs)
    def pack(self, **kwargs):
        if self["text"] not in ("*Required", "Auto correction"):
            kwargs["fill"]="x"
            kwargs["expand"]=1
        super().pack(**kwargs)

class R(tk.Radiobutton):
    def __init__(self, master, text, **kwargs):
        if "bg" not in kwargs:
            kwargs["bg"]=colors[3]
        if "font" not in kwargs:
            kwargs["font"]=app.font

        kwargs["anchor"]="w"
        super().__init__(master, text=text,**kwargs)
    def pack(self, **kwargs):
        if self["text"] not in ("*Required", "Auto correction"):
            kwargs["fill"]="x"
            kwargs["expand"]=1
        super().pack(**kwargs)

class Survey():
    def __init__(self):
        self.title="Untitled"
        self.survey_type="Quiz"
        self.time=-1
        self.participants=0
        self.pages=[IndexPage(), Page(1)]
    def getTitle(self):
        return self.title
    def setTitle(self, new_title):
        self.title=new_title

    def getType(self):
        return self.survey_type
    def setType(self, new_type):
        self.survey_type=new_type

    def getParticipantScore(self, survey_choices):
        if self.survey_type!="Quiz":
            return "N/A"
        score=0
        for i in range(1, self.getLength()):
            chosen_options=survey_choices[i-1]
            score+=self.getPage(i).getScore(chosen_options)
        return str(int( (score/ (self.getLength()-1) )*100) )+'%'
    
    def getTime(self):
        return "N/A"

    def addNewPage(self):
        if len(self.pages) < 100:
            self.pages.append(Page(len(self.pages)))
    
    def getPages(self):
        return self.pages
    def getPage(self, index):
        return self.pages[index]
    def getPageByTitle(self, page_title):
        return self.getPage(int(page_title[:2])-1)
    
    def updatePage(self, new_page, index):
        self.pages[index]=deepcopy(new_page)

    def removePage(self, page_index):
        del self.pages[page_index]
        for i in range(page_index+1, len(self.pages)+1):
            self.pages[i-1].index-=1
    
    def getLength(self):
        return len(self.pages)
    
    def getTitles(self):
        titles=()
        for p in self.pages:
            titles+=(p.getTitle(),)
        return titles

class Page():
    def __init__(self, index):
        self.index=index
        self.prompt=""
        self.answer_type="Singleline"
        self.auto_corrected=1
        self.available_options=[]
        self.valid_options=[]
        self.is_required=0

    def getPrompt(self):
        return self.prompt
    def setPrompt(self, new_prompt):
        self.prompt=new_prompt

    def getAvailableOptions(self):
        return self.available_options
    def addAvailableOption(self, new_option):
        self.available_options.append(new_option)
    def removeAvailableOption(self, option_value):
        self.available_options.remove(option_value)
    def clearAvailableOptions(self):
        self.available_options=[]

    def getValidOptions(self):
        return self.valid_options
    def addValidOption(self, new_option):
        self.valid_options.append(new_option)
    def removeValidOption(self, option_value):
        self.valid_options.remove(option_value)
    def clearValidOptions(self):
        self.valid_options=[]

    def getAnswerType(self):
        return self.answer_type
    def setAnswerType(self, new_type):
        self.answer_type=new_type

    def getTitle(self):
        return str(self.index+1).zfill(2)+' '+(self.prompt[:min(36, len(self.prompt))]).replace("\n", '')

    def getScore(self, chosen_options):
        if chosen_options and self.answer_type!="Checkbox":
            return chosen_options[0] in self.valid_options
        return chosen_options in self.valid_options

class IndexPage():
    def __init__(self):
        self.index=0
        self.content="Line 1\nLine 2\nLine 3\n"

    def getContent(self):
        return self.content
    def setContent(self, new_content):
        self.content=new_content

    def getType(self):
        return self.page_type

    def getTitle(self):
        return str(self.index+1).zfill(2)+' '+(self.content[:min(36, len(self.content))]).replace("\n", '')

class Database():
    def __init__(self):
        self.data={"surveys":{}, "making":{}, "made":{}, "mysubmissions":{}, "submissions":{}, "corrections":{}}

    def save(self):
        print("DATABASE - -")
        for k in self.data.keys():
            print(" "*4, k, ": : :")
            for kk in self.data[k].keys():
                print(" "*8, kk, "<<<")
                print(" "*8, self.data[k][kk], "- -")
        app.saveDatabaseAs(app.database_file_name)

    def getValidTitleIn(self, node):
        title="Untitled"
        while title in self.data[node]:
            title+=generatedCode()
        return title
    
    def hasSurvey(self, title):
        return title in self.data["surveys"]

    def addSurveyTo(self, survey, node):
        print("Added +")
        title=survey.getTitle()
        while title in self.data[node]:
            title+=generatedCode()
        survey.setTitle(title)
        self.data[node][title]=deepcopy(survey)
        if node == "made":
            self.data["submissions"][title]=[]
        if node in ("surveys", "made"):
            self.data["mysubmissions"][title]=[]
        self.save()
        return title

    def submitSurvey(self, survey, survey_choices):
        self.data["mysubmissions"][survey.getTitle()]=self.data["mysubmissions"][survey.getTitle()] + [tuple(survey_choices)]
        print("Submitted :", tuple(survey_choices))
        self.save()

    def submitToSurvey(self, survey_title, survey_choices):
        self.data["submissions"][survey_title]=self.data["submissions"][survey_title] + [tuple(survey_choices)]
        self.save()

    def getSurveys(self):
        return self.data["surveys"].values()

    def getSurvey(self, survey_title):
        return self.data["surveys"][survey_title]

    def deleteSurvey(self, survey_title):
        del self.data["surveys"][survey_title]
        self.save()
    
    def getMySubmissions(self):
        return self.data["mysubmissions"]

    def getMySubmission(self, survey_title):
        return self.data["mysubmissions"][survey_title]

    def getSubmissions(self, survey):
        return self.data["submissions"][survey.getTitle()]

    def getMakingTitles(self):
        return self.data["making"]

    def getMakingSurveys(self):
        return self.data["making"].values()

    def getMadeSurveys(self):
        return self.data["made"].values()

    def getSurveyFrom(self, survey_title, node):
        return self.data[node][survey_title]

    def updateSurveyIn(self, new_survey, survey_title, node):
        new_title=new_survey.getTitle()
        self.data[node][new_title]=new_survey
        if survey_title!=new_title:
            del self.data[node][survey_title]
        self.save()
    
    def removeSurveyFrom(self, survey, node):
        del self.data[node][survey.getTitle()]
        self.save()

class StartWindow():
    def __init__(self):
        self.root=F(app.root)

        self.F_root=F(self.root)

        L(self.F_root, text="VEY", font=("Terminal", 47, "bold")).pack(pady=160)
        B(self.F_root, text=f"START - VEY  v{app.version}", command=app.openNavigationWindow, width=40).pack()

        self.F_root.pack(fill="both", expand=1)

class NavigationWindow():
    def __init__(self):
        self.root=F(app.root)
        
        F_header=F(self.root, bg=colors[4])

        nav=tk.StringVar()
        nav.set(app.navigation_value)
        if nav.get()=="TAKE":
            nav.set("TOOK")
        M_navigation=tk.OptionMenu(F_header, nav, *("TAKE","MAKE","TOOK","MADE"), command=self.navigate)
        M_navigation.config(bg=colors[1], activebackground=colors[1], relief="flat")
        M_navigation.pack(side="left")

        F_header.pack(fill="x")
        
        self.F_child=F(self.root)

        self.navigate(nav.get())

    def navigate(self, nav):
        app.navigation_value=nav
        self.F_child.destroy()
        if nav=="TAKE":
            F_take=TakeFrame(self.root)
            self.F_child=F_take.root
        elif nav=="MAKE":
            F_make=MakeFrame(self.root)
            self.F_child=F_make.root
        elif nav=="MADE":
            F_made=MadeFrame(self.root)
            self.F_child=F_made.root
        else: #frame=="TOOK":
            F_took=TookFrame(self.root)
            self.F_child=F_took.root
        self.F_child.pack(fill="both", padx=8)

class TakeFrame():
    def __init__(self, master):
        self.root=F(master)
        
        F_add=F(self.root)
        B(F_add, text="+ IMPORT SURVEY", command=self.importSurvey, width=20).pack(fill="x")
        F_add.pack()
        
        self.F_surveys=F(self.root)
        
        self.refresh()
    
    def refresh(self):
        self.F_surveys.destroy()
        self.F_surveys=F(self.root)
        
        surveys=app.database.getSurveys()
        if surveys:
            labels=("Title", "Type", "Duration", "Pages")
            for i, label in enumerate(labels):
                L(self.F_surveys, text=label, font=app.font).grid(row=0, column=i, sticky='W')

            for i, survey in enumerate(surveys):
                color=colors[0]
                if i%2:
                    color=colors[1]
                L(self.F_surveys, text=survey.title, bg=color, fg="black").grid(row=i+1, column=0, sticky='W')
                L(self.F_surveys, text=survey.survey_type).grid(row=i+1, column=1, sticky='W')
                L(self.F_surveys, text=survey.getTime()).grid(row=i+1, column=2, sticky='W')
                L(self.F_surveys, text=survey.getLength()).grid(row=i+1, column=3, sticky='W')

                B(self.F_surveys, text="TAKE", bg=color, relief="raised", command=lambda survey=survey: app.openTakingWindow(survey)).grid(row=i+1, column=4)
        else:
            L(self.F_surveys, text="No survey to take", fg=colors[1], bg=colors[0]).pack(fill="x", expand=1, pady=16)
        self.F_surveys.pack(fill="x")

    def importSurvey(self):
        app.root.filename=filedialog.askopenfilename(initialdir = "C:\\", title = "Select file", filetypes = (("bin files","*.bin"),))
        file_name=app.root.filename
        if file_name:
            app.importSurvey(file_name)


class MakeFrame():
    def __init__(self, master):
        self.root=F(master)
    
        F_add=F(self.root)
        B(F_add, text="+ MAKE NEW SURVEY", font=app.font, command=self.beginMakingNewSurvey, width=20).pack(fill="x")
        F_add.pack()
        
        self.F_surveys=F(self.root)
        self.refresh()
    
    def refresh(self):
        self.F_surveys.destroy()
        self.F_surveys=F(self.root)
        surveys=app.database.getMakingSurveys()
        if surveys:
            labels=("Title", "Type", "Duration", "Pages")
            for i, label in enumerate(labels):
                L(self.F_surveys, text=label, font=app.font).grid(row=0, column=i, sticky='W')

            for i, survey in enumerate(surveys):
                color=colors[0]
                if i%2:
                    color=colors[1]
                L(self.F_surveys, text=survey.title, bg=color, fg="black").grid(row=i+1, column=0, sticky='W')
                L(self.F_surveys, text=survey.survey_type).grid(row=i+1, column=1, sticky='W')
                L(self.F_surveys, text=survey.getTime()).grid(row=i+1, column=2, sticky='W')
                L(self.F_surveys, text=survey.getLength()).grid(row=i+1, column=3, sticky='W')

                B(self.F_surveys, text="EDIT", bg=color, relief="raised", command=lambda survey=survey: app.openMakingWindow(survey)).grid(row=i+1, column=4)
                B(self.F_surveys, text="EXPORT", bg=color, relief="raised", command=lambda survey_title=survey.getTitle(): app.publishSurvey(survey_title)).grid(row=i+1, column=5)
                B(self.F_surveys, text="COPY", bg=color, relief="raised", command=lambda survey=survey: self.copySurvey(survey)).grid(row=i+1, column=6)

                def removeSurveyFunction(survey):
                    survey=deepcopy(survey)
                    def removeSurvey():
                        app.removeMakeSurvey(survey)
                        self.refresh()
                    return removeSurvey

                B(self.F_surveys, text="- DELETE", bg=color, relief="raised", command=removeSurveyFunction(survey)).grid(row=i+1, column=7)
        else:
            L(self.F_surveys, text="No survey is being made", fg=colors[1], bg=colors[0]).pack(fill="x", expand=1, pady=16)
        self.F_surveys.pack(fill="x")
    def copySurvey(self, survey):
        app.database.addSurveyTo(deepcopy(survey), "making")
        self.refresh()
    def beginMakingNewSurvey(self):
        new_survey=Survey()
        new_survey.setTitle(app.database.getValidTitleIn("making"))
        app.openMakingWindow(new_survey)

class TookFrame():
    def __init__(self, master):
        self.root=F(master)
        
        self.F_surveys=F(self.root)
        
        self.refresh()
    
    def refresh(self):
        self.F_surveys.destroy()
        self.F_surveys=F(self.root)
        
        submissions_titles=app.database.getMySubmissions()
        print("Submissions", len(submissions_titles))
        if submissions_titles:
            labels=("Title", "Type", "Score")
            for i, label in enumerate(labels):
                L(self.F_surveys, text=label).grid(row=0, column=i, sticky='W')
            
            i=0
            for survey_title in submissions_titles:
                survey=app.database.getSurvey(survey_title)
                survey_multiple_choices=app.database.getMySubmission(survey_title)
                print("Survey choices", len(survey_multiple_choices))
                for survey_choices in survey_multiple_choices:
                    color=colors[0]
                    if i%2:
                        color=colors[1]
                    score=survey.getParticipantScore(survey_choices)
                    score_color="yellow"
                    if score=="100%":
                        score_color="#4f9"
                    L(self.F_surveys, text=survey.title, bg=color, fg="black").grid(row=i+1, column=0, sticky='W')
                    L(self.F_surveys, text=survey.survey_type).grid(row=i+1, column=1, sticky='W')
                    L(self.F_surveys, text=score, bg=score_color, fg="black").grid(row=i+1, column=2, sticky='W')

                    #B(self.F_surveys, text="EXPORT CHOICES", bg=color, relief="raised", command=lambda survey=survey, survey_choices=survey_choices: app.exportChoices(survey, survey_choices)).grid(row=i+1, column=3)
                    
                    needs_correction=False
                    for j in range(1, survey.getLength()):
                        page=survey.getPage(j)
                        if not page.auto_corrected and not page.getValidOptions():
                            needs_correction=True
                            break
                    if False :#needs_correction:
                        B(self.F_surveys, text="IMPORT CORRECTION", bg=color, relief="raised", command=self.importCorrection).grid(row=i+1, column=3)
                    else:
                        B(self.F_surveys, text="CORRECTION", bg=color, relief="raised", command=lambda survey=survey, survey_choices=survey_choices: app.openCorrectionWindow(survey, survey_choices)).grid(row=i+1, column=3)

                    i+=1
        else:
            L(self.F_surveys, text="No taken surveys", fg=colors[1], bg=colors[0]).pack(fill="x", expand=1, pady=16)
        self.F_surveys.pack(fill="x")
    
    def importCorrection(self):
        app.root.filename=filedialog.askopenfilename(initialdir = "C:\\", title = "Select file", filetypes = (("bin files","*.bin"),))
        file_name=app.root.filename
        if file_name:
            app.importCorrection(file_name)
            self.refresh()

class MadeFrame():
    def __init__(self, master):
        self.root=F(master)
        
        self.F_surveys=F(self.root)
        
        self.refresh()
    
    def refresh(self):
        self.F_surveys.destroy()
        self.F_surveys=F(self.root)
        surveys=app.database.getMadeSurveys()
        if surveys:
            labels=("Title", "Type", "Participants", "Pages")
            for i, label in enumerate(labels):
                L(self.F_surveys, text=label, font=app.font).grid(row=0, column=i, sticky='W')

            for i, survey in enumerate(surveys):
                color=colors[0]
                if i%2:
                    color=colors[1]
                L(self.F_surveys, text=survey.title, bg=color, fg="black").grid(row=i+1, column=0, sticky='W')
                L(self.F_surveys, text=survey.survey_type).grid(row=i+1, column=1, sticky='W')
                L(self.F_surveys, text=survey.participants).grid(row=i+1, column=2, sticky='W')
                L(self.F_surveys, text=survey.getLength()).grid(row=i+1, column=3, sticky='W')
                """

                B(self.F_surveys, text="IMPORT CHOICES", bg=color, relief="raised", command=self.importSurveyChoices).grid(row=i+1, column=4)
                B(self.F_surveys, text="CORRECT", bg=color, relief="raised", command=lambda survey=survey: app.openCorrectingWindow(survey)).grid(row=i+1, column=5)
                B(self.F_surveys, text="EXPORT CORRECTION", bg=color, relief="raised", command=lambda survey=survey: app.printMadeSurvey(survey)).grid(row=i+1, column=6)
                B(self.F_surveys, text="INSIGHT", bg=color, relief="raised", command=lambda survey_title=survey.getTitle(): app.openInsightWindow(survey_title)).grid(row=i+1, column=7)
                """
        else:
            L(self.F_surveys, text="No made surveys", fg=colors[1], bg=colors[0]).pack(fill="x", expand=1, pady=16)
        self.F_surveys.pack(fill="x")

    def importSurveyChoices(self):
        app.root.filename=filedialog.askopenfilename(initialdir = "C:\\", title = "Select file", filetypes = (("bin files","*.bin"),))
        file_name=app.root.filename
        if file_name:
            app.importSurveyChoices(file_name)

class MakingWindow():
    def __init__(self, survey):
        self.root=F(app.root)

        self.F_root=F(self.root)

        self.survey=deepcopy(survey)
        self.survey_old_title=deepcopy(self.survey.getTitle())
        self.current_page=survey.getPage(0)

        self.buildHeader()

        self.buildNavigation()

        self.buildBody()

        self.displayIndexPage()
        
        self.buildFooter()
        
        self.refreshLabels()

        self.F_root.pack(fill="both", expand=1, padx=28, pady=8)

    def buildHeader(self):
        print("Function :", "buildHeader")
        # CRAETING A FRAME, LABEL, AND A BUTTON.
        F_header=F(self.F_root)
        self.L_survey_title=L(F_header, text=self.survey.title)
        self.L_message=L(F_header, text='', fg=colors[0])
        B(F_header, text="SAVE", command=self.closeWindow).pack(side="right")
        B(F_header, text="DISCARD", fg=colors[1], bg=colors[0], command=self.discard).pack(side="right")
        self.L_message.pack(side="right")
        # PACKING
        self.L_survey_title.pack(side="left")
        F_header.pack(fill="x", side="top")
        F(self.F_root, bg=colors[3], height="1").pack(fill='x', side="top", pady=4)

    def buildNavigation(self):
        print("Function :", "buildNavigation")
        # CREATING A FRAME, PREPARING A VARIABLE, AND AN OPTIONS MENU
        F_navigation=F(self.F_root, bg=colors[4])
        self.Var_title=tk.StringVar()
        self.M_titles = tk.OptionMenu(F_navigation, self.Var_title, "value")
        self.M_titles.config(bg=colors[1], activebackground=colors[1], relief="flat")

        # PACKING
        self.M_titles.pack(side="left")
        F_navigation.pack(fill="x", side="top")

    def buildBody(self):
        print("Function :", "buildBody")
        # CREATING FRAMES
        self.F_body=F(self.F_root)        
        self.F_in_body=F(self.F_body)
        
        # PREPARING VARIABLES
        self.Var_radio=tk.StringVar()
        self.Var_is_required=tk.IntVar()
        self.checkboxed=set()
        
        # PACKING
        self.F_in_body.pack(fill="both")
        self.F_body.pack(fill="both", side="top", padx=8, pady=8)

    def buildFooter(self):
        print("Function :", "buildFooter")
        # CREATING A FRAME AND A LABEL
        F_footer=F(self.F_root)
        self.L_page_counter=L(F_footer, font=app.font)

        def changePageIndexBy(variation):
            page_index=self.current_page.index
            if (variation <= 0 and page_index != 0) or (variation >= 0 and page_index != self.survey.getLength()-1):
                self.navigateToPage(self.survey.getPage(page_index+variation).getTitle())
            self.refreshLabels()
        
        def removeCurrentPage():
            page_index=self.current_page.index
            if page_index:
                warning_msg="Are you sure to delete this page !"
                if self.L_message["text"] == warning_msg:
                    changePageIndexBy(-1)
                    self.survey.removePage(page_index)
                    app.database.updateSurveyIn(deepcopy(self.survey), self.survey.getTitle(), "making")
                    
                    self.refreshLabels()
                else:
                    self.L_message["text"]=warning_msg

        
        def addNewPage():
            self.survey.addNewPage()
            changePageIndexBy(self.survey.getLength()-1-self.current_page.index)
            self.refreshLabels()

        # CREATING BUTTONS
        B_previous=B(F_footer, text="<", command=lambda: changePageIndexBy(-1), width=2)
        B_remove_current_page=B(F_footer, text="- DELETE", fg=colors[1], bg=colors[0], command=removeCurrentPage)
        B_next=B(F_footer, text=">", command=lambda: changePageIndexBy(1), width=2)
        B_add_new_page=B(F_footer, text="+ PAGE", command=addNewPage)

        # PACKING
        B_previous.pack(side="left")
        B_next.pack(side="left")
        B_add_new_page.pack(side="left")
        B_remove_current_page.pack(side="right")
        self.L_page_counter.pack(expand=1, side="right")

        F_footer.pack(fill="x", side="bottom")
        F(self.F_root, bg=colors[3], height="1").pack(fill='x', side="bottom", pady=4)

    def refreshLabels(self):
        print("Function :", "refreshLabels")
        # UPDATING LABELS
        self.L_survey_title["text"]=self.survey.getTitle()
        self.L_message["text"]=''
        self.L_page_counter["text"]=f"Page {self.current_page.index+1}/{self.survey.getLength()}"

        # UPDATING THE OUTLINE MENU AND ITS VARIABLE
        menu=self.M_titles["menu"]
        menu.delete(0, "end")
        for title in self.survey.getTitles():
            def toPage(value):
                self.Var_title.set(value)
                self.navigateToPage(value)
                self.refreshLabels()
            menu.add_command(label=title, command=lambda value=title: toPage(value))
        self.Var_title.set(self.current_page.getTitle())

    def refreshVariables(self):
        print("Function :", "refreshVariables")
        self.Var_radio.set('')
        self.checkboxed=set()
        if self.current_page.auto_corrected:
            valid_options=self.current_page.getValidOptions()
            if self.current_page.getAnswerType() in ("Radio", "Two options") and valid_options:
                self.Var_radio.set(valid_options[0])
            if self.current_page.getAnswerType()=="Checkbox":
                if valid_options:
                    self.checkboxed=deepcopy(valid_options[0])

    def displayIndexPage(self):
        print("Function :", "displayIndexPage")
        # PREPARING VARIABLES
        self.Var_survey_type=tk.StringVar()
        survey_types=("Form", "Survey", "Quiz")
        self.Var_survey_type.set(self.survey.survey_type)
        
        # CREATING INPUT ELEMENTS
        self.E_survey_title=tk.Entry(self.F_in_body, width=36, bg=colors[3], insertbackground=colors[1], fg=colors[1])
        self.M_survey_type=tk.OptionMenu(self.F_in_body, self.Var_survey_type, *survey_types)
        self.M_survey_type.config(bg=colors[1], activebackground=colors[1], relief="flat")
        self.T_index_content=tk.Text(self.F_in_body, width=75, height=16, fg=colors[1], bg=colors[3], insertbackground=colors[1])

        # GRIDING WITH LABELS
        L(self.F_in_body, text="Type :").grid(row=0, column=0, sticky='W')
        self.M_survey_type.grid(row=0, column=1, sticky='W')
        L(self.F_in_body, text="Title :").grid(row=1, column=0, sticky='W')
        self.E_survey_title.grid(row=1, column=1, sticky='W')
        L(self.F_in_body, text="Index :").grid(row=2, column=0, sticky='W')
        self.T_index_content.grid(row=3, column=0, columnspan=2, sticky='W')

        # INSERTING PREWRITTEN TEXT
        self.E_survey_title.insert(0, self.survey.getTitle())
        self.T_index_content.insert("1.0", self.current_page.getContent())

    def saveIndexChanges(self):
        print("Function :", "saveIndexChanges")
        # UPDATE THE TITLE AND TYPE OF SURVEY
        self.survey.setTitle(self.E_survey_title.get())
        self.survey.setType(self.Var_survey_type.get())
        
        # UPDATE INDEX PAGE CONTENT
        text_box_content=self.T_index_content.get("1.0", "end")
        self.current_page.setContent(text_box_content[:-1])
        self.survey.updatePage(self.current_page, 0)

    def navigateToPage(self, page_title):
        print("Function :", "navigateToPage", page_title)
        if page_title[:2] == self.current_page.getTitle()[:2]:
            return

        if self.current_page.index:
            self.saveCurrentPageChanges()

            # NEW OPTIONS FRAME
            self.F_options.destroy()
            self.F_options=F(self.F_in_body)
            self.F_options.pack(fill='x', pady=24)

            # GET THE NEW PAGE
            self.current_page=self.survey.getPageByTitle(page_title)
            
            if self.current_page.index:
                # NEW QUESTION PROMPT
                self.T_prompt.delete("1.0", "end")
                self.T_prompt.insert("1.0", deepcopy(self.current_page.getPrompt()))
                
                # PREPARING VARIABLES
                self.Var_answer_type.set(self.current_page.getAnswerType())
                self.Var_is_required.set(self.current_page.is_required)
                
                # DECIDE WETHER TO DISPLAY THE AUTO CORRECTION BUTTON
                if self.survey.getType()=="Quiz":
                    self.Var_auto_corrected.set(self.current_page.auto_corrected)
                self.refreshVariables()

                self.displayCurrentPage()
            else:
                # PREPARE THE MAIN FRAME TO DISPLAY THE CONTENT OF THE INDEX
                self.F_in_body.destroy()
                self.F_in_body=F(self.F_body)
                self.F_in_body.pack(fill="both")
                self.displayIndexPage()
        else:
            # SAVE INDEX CHANGES
            self.saveIndexChanges()

            # PREPARE THE MAIN FRAME TO DISPLAY THE CONTENT OF A PAGE
            self.F_in_body.destroy()
            self.F_in_body=F(self.F_body)
            self.F_in_body.pack(fill="both")

            # GET THE NEW PAGE
            self.current_page=self.survey.getPageByTitle(page_title)
            # DISPLAY A QUESTION TEXT BOX IN A FRAME
            F_prompt=F(self.F_in_body)
            self.T_prompt=tk.Text(F_prompt, width=75, height=5, bg=colors[3], insertbackground=colors[1], fg=colors[1])
            
            self.T_prompt.insert("1.0", deepcopy(self.current_page.getPrompt()))
            
            self.T_prompt.pack(side="left")
            F_prompt.pack(fill='x')
            
            # DISPLAY ANSWER OPTIONS
            F_answer_settings=F(self.F_in_body)

            answer_types=("Checkbox", "Radio", "Two options", "Multiline", "Singleline")
            self.Var_answer_type=tk.StringVar()
            self.Var_answer_type.set(self.current_page.getAnswerType())

            M_answer_types=tk.OptionMenu(F_answer_settings, self.Var_answer_type, *answer_types, command=lambda new_answer_type: self.adaptToNewAnswerType(new_answer_type))
            M_answer_types.config(bg=colors[1], activebackground=colors[1], relief="flat")
            M_answer_types.pack(side="left")

            if self.survey.getType()=="Quiz":
                self.Var_auto_corrected=tk.IntVar()
                self.Var_auto_corrected.set(self.current_page.auto_corrected)
                def autoCrtChecked():
                    return
                    auto_corrected=self.Var_auto_corrected.get()
                    self.current_page.auto_corrected=auto_corrected
                    if auto_corrected:
                        self.Var_radio.set('')
                        self.checkboxed=set()
                C(F_answer_settings, variable=self.Var_auto_corrected, text="Auto correction", bg="#4f9", font=app.font, command=autoCrtChecked).pack(side="right")

            self.Var_is_required.set(self.current_page.is_required)
            def requiredChecked():
                self.current_page.is_required=self.Var_is_required.get()
            C(F_answer_settings, variable=self.Var_is_required, text="*Required", font=app.font, command=requiredChecked).pack(side="right")

            F_answer_settings.pack(fill="x")

            self.F_options=F(self.F_in_body)
            self.F_options.pack(fill='x', pady=24)
            self.refreshVariables()

            self.displayCurrentPage()

    def displayCurrentPage(self):
        print("Function :", "displayCurrentPage")
        answer_type=self.current_page.getAnswerType()
        if answer_type in ("Checkbox","Radio","Two options"):
            F_input=F(self.F_options)
            E_new_option_value=tk.Entry(F_input, width=36, bg=colors[3], insertbackground=colors[1], fg=colors[1])

            F_input.pack(expand=1)
            E_new_option_value.pack(side="left")
            
            def addOption(new_option_value=''):
                if not new_option_value:
                    new_option_value=E_new_option_value.get()
                if new_option_value in self.current_page.getAvailableOptions() or new_option_value=='':
                    return

                if answer_type=="Two options":
                    maxsize_options=2
                else:
                    maxsize_options=6
                
                if len(self.current_page.getAvailableOptions()) < maxsize_options:

                    F_option=F(self.F_options)
                    if answer_type=="Checkbox":

                        Var_checkbox=tk.IntVar()
                        Var_checkbox.set(new_option_value in self.checkboxed)
                        def optionChecked():
                            if Var_checkbox.get():
                                self.checkboxed.add(new_option_value)
                            else:
                                self.checkboxed.remove(new_option_value)
                        new_option=C(F_option, variable=Var_checkbox, text=new_option_value, font=app.font, command=optionChecked)
                    
                    else:

                        new_option=R(F_option, variable=self.Var_radio, value=new_option_value, text=new_option_value, font=app.font)

                    def removeOption():
                        option_value=new_option_value
                        E_new_option_value.delete(0, "end")
                        E_new_option_value.insert(0, option_value)

                        self.current_page.getAvailableOptions().remove(option_value)
                        if option_value in self.current_page.getValidOptions():
                            self.current_page.removeValidOption(option_value)
                        F_option.destroy()

                        if answer_type=="Checkbox" and option_value in self.checkboxed:
                            self.checkboxed.remove(option_value)
                        elif option_value == self.Var_radio.get():
                            self.Var_radio.set('')

                    new_option.pack(side="left")
                    B(F_option, text='-', font=app.font, fg=colors[1], bg=colors[0], command=removeOption, width=2).pack(side="right")
                    F_option.pack(fill="x", pady=2)


                    self.current_page.addAvailableOption(new_option_value)
            

            B(F_input, text="+", font=app.font, command=addOption, width=2).pack(side="left")

            available_options=deepcopy(self.current_page.getAvailableOptions())
            self.current_page.clearAvailableOptions()
            for value in available_options:
                addOption(value)
        
        elif answer_type=="Multiline":

            new_option=tk.Text(self.F_options, width=75, height=5, bg=colors[3], insertbackground=colors[1], fg=colors[1])
            valid_options=self.current_page.getValidOptions()
            if valid_options:
                new_option.insert("1.0", valid_options[0])
            self.T_option=new_option

            new_option.pack()
        
        else:

            new_option=tk.Entry(self.F_options, width=36, bg=colors[3], insertbackground=colors[1], fg=colors[1])
            valid_options=self.current_page.getValidOptions()
            if valid_options:
                new_option.insert(0, valid_options[0])
            self.E_option=new_option

            new_option.pack()

    def saveCurrentPageChanges(self):
        print("Function :", "saveCurrentPageChanges")
        # APPLY CHANGES TO THE CURRENT PAGE
        text_box_content=self.T_prompt.get("1.0", "end")[:-1]
        self.current_page.setPrompt(text_box_content)
        answer_type=self.current_page.getAnswerType()

        self.current_page.clearValidOptions()
        if self.current_page.auto_corrected:
            valid_options=self.current_page.getValidOptions()
            if answer_type == "Checkbox":
                valid_options.append(deepcopy(self.checkboxed))
            else:
                if answer_type in ("Radio", "Two options"):
                    value=self.Var_radio.get()
                    if value:
                        valid_options.append(value)

                elif answer_type == "Singleline":
                    value=self.E_option.get()
                    if value:
                        valid_options.append(value)

                else:
                    value=self.T_option.get("1.0", "end")[:-1]
                    if value:
                        valid_options.append(value)

        # UPDATE THE PAGE
        self.survey.updatePage(self.current_page, self.current_page.index)
        print(valid_options, self.current_page.valid_options)

    def adaptToNewAnswerType(self, new_answer_type):
        print("Function :", "adaptToNewAnswerType")
        if new_answer_type == self.current_page.getAnswerType():
            return
        # REMOVE THE PREVIOUS OPTIONS FRAME, THEN CREATE A NEW ONE
        self.F_options.destroy()
        self.F_options=F(self.F_body)
        self.F_options.pack(fill='x', pady=24)
        
        # MAKE THE PROPERTIES OF THE CURRENT PAGE FIT WITH THE NEW TYPE
        self.current_page.clearAvailableOptions()
        self.current_page.setAnswerType(new_answer_type)

        self.current_page.clearValidOptions()

        self.displayCurrentPage()

    def saveSurveyChanges(self):
        print("Function :", "saveSurveyChanges")
        if self.current_page.index:
            self.saveCurrentPageChanges()
        else:
            self.saveIndexChanges()

    def discard(self):
        print("Function :", "discard")
        warning_msg="Are you sure to discard changes !"
        if self.L_message["text"] == warning_msg:
            app.openNavigationWindow()
        else:
            self.L_message["text"]=warning_msg

    def closeWindow(self):
        print("Function :", "closeWindow")
        self.saveSurveyChanges()
        for page in self.survey.getPages()[1:]:
            if not page.getValidOptions() and page.auto_corrected:
                self.L_message["text"]=f"Choose a valid option in page {page.index+1} !"
                return
        if self.survey.getLength()>1:
            titles=app.database.getMakingTitles()
            old_title=self.survey_old_title
            new_title=self.survey.getTitle()
            if old_title in titles: # ALREADY EXISTS
                if old_title != new_title and new_title in titles: # THE OLD TITLE HAS CHANGED
                    self.L_message["text"]="Title is already taken !"
                else:
                    app.database.updateSurveyIn(deepcopy(self.survey), self.survey_old_title, "making")
                    
                    app.openNavigationWindow()
            else: # NEW SURVEY
                if new_title in titles: # THE NEW TITLE IS CHOSEN
                    self.L_message["text"]="Title is already taken !"
                else:
                    app.database.addSurveyTo(self.survey, "making")
                    
                    app.openNavigationWindow()
        else:
            self.L_message["text"]="Add at least one question !"


class TakingWindow():
    def __init__(self, survey):
        self.root=F(app.root)

        self.F_root=F(self.root)

        self.survey=survey
        self.current_page=survey.getPage(0)
        self.survey_choices=[ [] for i in range(self.survey.getLength()-1) ]
        self.chosen_options=[]

        self.buildHeader()

        self.buildNavigation()

        self.buildBody()

        self.displayIndexPage()
        
        self.buildFooter()
        
        self.refreshLabels()

        self.F_root.pack(fill="both", expand=1, padx=28, pady=8)

    def buildHeader(self):
        # CRAETING A FRAME, LABEL, AND A BUTTON.
        F_header=F(self.F_root)
        self.L_survey_title=L(F_header, text=self.survey.title)
        self.L_message=L(F_header, text='', fg=colors[0])
        B(F_header, text="SUBMIT", command=self.closeWindow).pack(side="right")
        B(F_header, text="DISCARD", fg=colors[1], bg=colors[0], command=self.discard).pack(side="right")
        self.L_message.pack(side="right")
        # PACKING
        self.L_survey_title.pack(side="left")
        F_header.pack(fill="x", side="top")
        F(self.F_root, bg=colors[3], height="1").pack(fill='x', side="top", pady=4)

    def buildNavigation(self):
        # CREATING A FRAME, PREPARING A VARIABLE, AND AN OPTIONS MENU
        F_navigation=F(self.F_root, bg=colors[4])
        self.Var_title=tk.StringVar()
        M_titles = tk.OptionMenu(F_navigation, self.Var_title, "value")
        M_titles.config(bg=colors[1], activebackground=colors[1], relief="flat")

        menu=M_titles["menu"]
        menu.delete(0, "end")
        for title in self.survey.getTitles():
            def toPage(value):
                self.Var_title.set(value)
                self.navigateToPage(value)
                self.refreshLabels()
            menu.add_command(label=title, command=lambda value=title: toPage(value))
        self.Var_title.set(self.current_page.getTitle())

        # PACKING
        M_titles.pack(side="left")
        F_navigation.pack(fill="x", side="top")

    def buildBody(self):
        # CREATING FRAMES
        self.F_body=F(self.F_root)        
        self.F_in_body=F(self.F_body)
        
        # PREPARING VARIABLES
        self.Var_radio=tk.StringVar()
        
        # PACKING
        self.F_in_body.pack(fill="both")
        self.F_body.pack(fill="both", side="top", padx=8, pady=8)

    def buildFooter(self):
        # CREATING A FRAME AND A LABEL
        F_footer=F(self.F_root)
        self.L_page_counter=L(F_footer, font=app.font)

        def changePageIndexBy(variation):
            page_index=self.current_page.index
            if (variation <= 0 and page_index != 0) or (variation >= 0 and page_index != self.survey.getLength()-1):
                self.navigateToPage(self.survey.getPage(page_index+variation).getTitle())
            self.refreshLabels()

        # CREATING BUTTONS
        B_previous=B(F_footer, text="<", command=lambda: changePageIndexBy(-1), width=2)
        B_next=B(F_footer, text=">", command=lambda: changePageIndexBy(1), width=2)

        # PACKING
        B_previous.pack(side="left")
        B_next.pack(side="left")
        self.L_page_counter.pack(expand=1, side="right")

        F_footer.pack(fill="x", side="bottom")
        F(self.F_root, bg=colors[3], height="1").pack(fill='x', side="bottom", pady=4)

    def refreshLabels(self):
        # UPDATING LABELS
        self.L_message["text"]=''
        self.L_page_counter["text"]=f"Page {self.current_page.index+1}/{self.survey.getLength()}"
        self.Var_title.set(self.current_page.getTitle())

    def displayIndexPage(self):
        T_index=tk.Text(self.F_in_body, fg=colors[1], bg=colors[4], height="20")
        T_index.insert("1.0", self.current_page.getContent())
        T_index["state"]="disabled"
        T_index.pack(fill='x', expand=1)

    def navigateToPage(self, page_title):
        if page_title[:2] == self.current_page.getTitle()[:2]:
            return
        
        if self.current_page.index:
            self.saveCurrentPageChanges()

        self.F_in_body.destroy()
        self.F_in_body=F(self.F_body)
        self.F_in_body.pack(fill='both', pady=24)

        # GET THE NEW PAGE
        self.current_page=self.survey.getPageByTitle(page_title)

        if self.current_page.index:
            self.chosen_options=deepcopy(self.survey_choices[self.current_page.index-1])
            self.survey_choices[self.current_page.index-1]=[]
            # DISPLAY A QUESTION TEXT BOX IN A FRAME
            T_prompt=tk.Text(self.F_in_body, fg=colors[1], bg=colors[4], height="7")
            T_prompt.insert("1.0", self.current_page.getPrompt())
            T_prompt["state"]="disabled"
            T_prompt.pack(fill='x', expand=1)

            F_answer_properties=F(self.F_in_body)
            if self.current_page.is_required:
                L(F_answer_properties, text="*Required", font=app.font, fg=colors[0]).pack(side="right")
            F_answer_properties.pack(fill="x")

            self.F_options=F(self.F_in_body)
            self.F_options.pack(fill='x')

            self.displayCurrentPage()

        else:
            # PREPARE THE MAIN FRAME TO DISPLAY THE CONTENT OF THE INDEX
            self.F_in_body.destroy()
            self.F_in_body=F(self.F_body)
            self.F_in_body.pack(fill='both', pady=24)
            self.displayIndexPage()

    def displayCurrentPage(self):
        answer_type=self.current_page.getAnswerType()
        if answer_type in ("Checkbox","Radio","Two options"):
            self.Var_radio.set('')
            if self.chosen_options:
                self.Var_radio.set(self.chosen_options[0])
            def addOption(new_option_value):
                F_option=F(self.F_options)
                if answer_type=="Checkbox":

                    Var_checkbox=tk.IntVar()
                    Var_checkbox.set(new_option_value in self.chosen_options)
                    def optionChecked():
                        if Var_checkbox.get():
                            self.chosen_options.append(new_option_value)
                        else:
                            self.chosen_options.remove(new_option_value)
                    new_option=C(F_option, variable=Var_checkbox, text=new_option_value, command=optionChecked)
                
                else:
                    new_option=R(F_option, variable=self.Var_radio, value=new_option_value, text=new_option_value)

                new_option.pack(side="left")
                F_option.pack(fill="x", pady=2)

            for value in self.current_page.getAvailableOptions():
                addOption(value)
        
        elif answer_type=="Multiline":

            new_option=tk.Text(self.F_options, width=75, height=5, fg=colors[1], bg=colors[3], insertbackground=colors[1])
            if self.chosen_options:
                new_option.insert("1.0", self.chosen_options[0])
            self.T_option=new_option

            new_option.pack()
        
        else:

            new_option=tk.Entry(self.F_options, width=36, fg=colors[1], bg=colors[3], insertbackground=colors[1])
            if self.chosen_options:
                new_option.insert(0, self.chosen_options[0])
            self.E_option=new_option

            new_option.pack()

    def saveCurrentPageChanges(self):
        # APPLY CHANGES TO THE CURRENT PAGE
        answer_type=self.current_page.getAnswerType()
        if answer_type != "Checkbox":
            if self.chosen_options:
                del self.chosen_options[0]
            
            if answer_type in ("Radio", "Two options"):
                value=self.Var_radio.get()
                if value:
                    self.chosen_options.append(value)

            elif answer_type == "Singleline":
                value=self.E_option.get()
                if value:
                    self.chosen_options.append(value)

            else:
                value=self.T_option.get("1.0", "end")[:-1]
                if value:
                    self.chosen_options.append(value)

            self.survey_choices[self.current_page.index-1]=deepcopy(self.chosen_options)
        else:
            self.survey_choices[self.current_page.index-1]=deepcopy(set(self.chosen_options))

    def saveSurveyChanges(self):
        if self.current_page.index:
            self.saveCurrentPageChanges()

    def discard(self):
        warning_msg="Are you sure to discard changes !"
        if self.L_message["text"] == warning_msg:
            app.openNavigationWindow()
        else:
            self.L_message["text"]=warning_msg

    def closeWindow(self):
        self.saveSurveyChanges()
        for i, chosen_options in enumerate(self.survey_choices):
            if not chosen_options and self.survey.getPage(i+1).is_required:
                self.L_message["text"]=f"Choose an option in page {i+2} !"
                return

        for page in self.survey.getPages()[1:]:
            if page.getAnswerType()=="Checkbox":
                self.survey_choices[page.index-1]=set(self.survey_choices[page.index-1])

        app.database.submitSurvey(self.survey, deepcopy(self.survey_choices))
        app.openNavigationWindow()


class CorrectionWindow(TakingWindow):
    def __init__(self, survey, survey_choices):
        self.root=F(app.root)

        self.F_root=F(self.root)

        self.survey=survey
        self.current_page=survey.getPage(0)
        self.survey_choices=survey_choices
        self.chosen_options=[]

        self.buildHeader()

        self.buildNavigation()

        self.buildBody()

        self.displayIndexPage()
        
        self.buildFooter()
        
        self.refreshLabels()

        self.F_root.pack(fill="both", expand=1, padx=28, pady=8)

    def buildHeader(self):
        # CRAETING A FRAME, LABEL, AND A BUTTON.
        F_header=F(self.F_root)
        self.L_survey_title=L(F_header, text=self.survey.title)
        B(F_header, text="DONE", command=self.closeWindow).pack(side="right")

        # PACKING
        self.L_survey_title.pack(side="left")
        F_header.pack(fill="x", side="top")
        F(self.F_root, bg=colors[3], height="1").pack(fill='x', side="top", pady=4)

    def refreshLabels(self):
        # UPDATING PAGE COUNTER LABEL
        self.L_page_counter["text"]=f"Page {self.current_page.index+1}/{self.survey.getLength()}"
        self.Var_title.set(self.current_page.getTitle())

    def refreshVariables(self):
        print("Function :", "refreshVariables")
        self.Var_radio.set('')
        if self.current_page.getAnswerType() in ("Radio", "Two options") and self.chosen_options:
            self.Var_radio.set(self.chosen_options[0])

    def navigateToPage(self, page_title):
        if page_title[:2] == self.current_page.getTitle()[:2]:
            return

        self.F_in_body.destroy()
        self.F_in_body=F(self.F_body)
        self.F_in_body.pack(fill='both', pady=24)

        # GET THE NEW PAGE
        self.current_page=self.survey.getPageByTitle(page_title)

        if self.current_page.index:
            self.chosen_options=self.survey_choices[self.current_page.index-1]
            # DISPLAY A QUESTION TEXT BOX IN A FRAME
            T_prompt=tk.Text(self.F_in_body, fg=colors[1], bg=colors[4], height="7")
            T_prompt.insert("1.0", self.current_page.getPrompt())
            T_prompt["state"]="disabled"
            T_prompt.pack(fill='x', expand=1)

            F_answer_properties=F(self.F_in_body)
            if self.current_page.is_required:
                L(F_answer_properties, text="*Required", font=app.font, fg=colors[0]).pack(side="right")
            F_answer_properties.pack(fill="x")

            self.F_options=F(self.F_in_body)
            self.F_options.pack(fill='x')
            
            self.refreshVariables()
            self.displayCurrentPage()

        else:
            # PREPARE THE MAIN FRAME TO DISPLAY THE CONTENT OF THE INDEX
            self.F_in_body.destroy()
            self.F_in_body=F(self.F_body)
            self.F_in_body.pack(fill='both', pady=24)
            self.displayIndexPage()

    def displayCurrentPage(self):
        auto_corrected=self.current_page.auto_corrected
        valid_options=self.current_page.getValidOptions()
        answer_type=self.current_page.getAnswerType()
        if answer_type in ("Checkbox","Radio","Two options"):
            def addOption(new_option_value):
                is_chosen=new_option_value in self.chosen_options
                color=colors[3]
                if auto_corrected:
                    if answer_type=="Checkbox":
                        is_valid=new_option_value in valid_options[0]
                    else:
                        is_valid=new_option_value in valid_options
                    if is_valid:
                        if is_chosen:
                            color="#4f9"
                        else:
                            color="#f77"
                    elif is_chosen:
                        color="#f77"
                else:
                    is_valid=self.chosen_options in valid_options
                    if is_chosen:
                        if is_valid:
                            color="#4f9"
                        else:
                            color="#f77"

                F_option=F(self.F_options)
                if answer_type=="Checkbox":
                    Var_checkbox=tk.IntVar()
                    Var_checkbox.set(is_chosen)
                    cd=lambda: Var_checkbox
                    new_option=C(F_option, variable=Var_checkbox, text=new_option_value, font=app.font, disabledforeground="black", bg=color, state="disabled", command=cd)

                else:
                    if self.chosen_options:
                        self.Var_radio.set(self.chosen_options[0])
                    new_option=R(F_option, variable=self.Var_radio, value=new_option_value, text=new_option_value, font=app.font, disabledforeground="black", bg=color, state="disabled")

                new_option.pack(side="left")
                F_option.pack(fill="x", pady=2)

            for value in self.current_page.getAvailableOptions():
                addOption(value)
        
        elif answer_type=="Multiline":
            if self.chosen_options:
                is_valid=self.chosen_options[0] in valid_options
                if is_valid:
                    color="#4f9"
                else:
                    color="#f77"
                T_choice=tk.Text(self.F_in_body, bg=color, height="3")
                T_choice.insert("1.0", self.chosen_options[0])
                T_choice["state"]="disabled"
                T_choice.pack(fill='x')

            if auto_corrected:
                T_answer=tk.Text(self.F_in_body, bg="#4f9", height="3")
                T_answer.insert("1.0", self.chosen_options[0])
                T_answer["state"]="disabled"
                T_answer.pack(fill='x')

        else:
            if self.chosen_options:
                is_valid=self.chosen_options[0] in valid_options
                if is_valid:
                    color="#4f9"
                else:
                    color="#f77"
                L(self.F_in_body, text=self.chosen_options[0], bg=color, fg="black").pack(fill='x')

            if auto_corrected:
                L(self.F_in_body, text=valid_options[0], bg="#4f9", fg="black").pack(fill='x')

    def closeWindow(self):
        app.openNavigationWindow()


class CorrectingWindow(TakingWindow):
    def __init__(self, survey):
        self.root=F(app.root)

        self.F_root=F(self.root)

        self.survey=survey
        for i in range(1, self.survey.getLength()):
            page=self.survey.getPage(i)
            if not page.auto_corrected:
                self.current_page=survey.getPage(i)
                break

        self.submissions=app.database.getSubmissions(self.survey)

        self.survey_valid_choices={}
        self.corrected_submissions={}

        self.survey_choices=self.submissions[0]
        self.chosen_options=self.survey_choices[self.current_page.index-1]

        self.buildHeader()

        self.buildNavigation()

        self.buildBody()

        self.navigateToPage(self.current_page.getTitle())
        
        self.buildFooter()
        
        self.refreshLabels()

        self.F_root.pack(fill="both", expand=1, padx=28, pady=8)

    def buildHeader(self):
        # CRAETING A FRAME, LABEL, AND A BUTTON.
        F_header=F(self.F_root)
        self.L_survey_title=L(F_header, text=self.survey.title)
        self.L_message=L(F_header, text='', fg=colors[0])
        B(F_header, text="SAVE", command=self.closeWindow).pack(side="right")
        B(F_header, text="DISCARD", command=self.discard).pack(side="right")
        self.L_message.pack(side="right")
        # PACKING
        self.L_survey_title.pack(side="left")
        F_header.pack(fill="x", side="top")

    def buildNavigation(self):
        # CREATING A FRAME, PREPARING A VARIABLE, AND AN OPTIONS MENU
        F_navigation=F(self.F_root, bg=colors[4])
        self.Var_title=tk.StringVar()
        M_titles = tk.OptionMenu(F_navigation, self.Var_title, "value")
        M_titles.config(bg=colors[1], activebackground=colors[1], relief="flat")

        menu=M_titles["menu"]
        menu.delete(0, "end")
        for i, title in enumerate(self.survey.getTitles()):
            if i and not self.survey.getPage(i).auto_corrected:
                self.corrected_submissions[i]=0
                self.survey_valid_choices[i]=[]
                def toPage(value):
                    self.Var_title.set(value)
                    self.navigateToPage(value)
                    self.refreshLabels()
                menu.add_command(label=title, command=lambda value=title: toPage(value))
        self.Var_title.set(self.current_page.getTitle())

        # PACKING
        M_titles.pack(side="left")
        F_navigation.pack(fill="x", side="top")

    def refreshLabels(self):
        # UPDATING PAGE COUNTER LABEL
        self.L_message["text"]=''
        self.L_page_counter["text"]=f"Page {self.current_page.index+1}/{self.survey.getLength()}"
        self.Var_title.set(self.current_page.getTitle())

    def navigateToPage(self, page_title):
        if page_title[:2] == self.current_page.getTitle()[:2]:
            return

        self.F_in_body.destroy()
        self.F_in_body=F(self.F_body)
        self.F_in_body.pack(fill='both', pady=24)

        # GET THE NEW PAGE
        self.current_page=self.survey.getPageByTitle(page_title)

        self.chosen_options=self.survey_choices[self.current_page.index-1]
        # DISPLAY A QUESTION TEXT BOX IN A FRAME
        multilineLabel(self.F_in_body, self.current_page.getPrompt()).pack(fill='x')

        F_answer_properties=F(self.F_in_body)
        if self.current_page.is_required:
            L(F_answer_properties, text="*Required", fg="red").pack(side="right")
        F_answer_properties.pack(fill="x")

        self.F_options=F(self.F_in_body)
        self.F_options.pack(fill='x', pady=24)

        self.displayCurrentPage()

    def buildFooter(self):
        # CREATING A FRAME AND A LABEL
        F_footer=F(self.F_root)
        self.L_page_counter=L(F_footer)

        def changePageIndexBy(variation):
            page_index=self.current_page.index
            next_page_index=page_index
            if (variation <= 0 and page_index != 1):
                for i in range(1, page_index):
                    if not self.survey.getPage(i).auto_corrected:
                        next_page_index=i
                        break
            elif (variation >= 0 and page_index + 1 < self.survey.getLength()):
                for i in range(page_index+1, self.survey.getLength()):
                    if not self.survey.getPage(i).auto_corrected:
                        next_page_index=i
                        break
            self.navigateToPage(self.survey.getPage(next_page_index).getTitle())
            self.refreshLabels()

        # CREATING BUTTONS
        B_previous=B(F_footer, text="<", command=lambda: changePageIndexBy(-1), width=2)
        B_next=B(F_footer, text=">", command=lambda: changePageIndexBy(1), width=2)

        # PACKING
        B_previous.pack(side="left")
        B_next.pack(side="right")
        self.L_page_counter.pack(expand=1, side="right")
        F_footer.pack(fill="x", side="bottom")

    def displayCurrentPage(self):
        self.chosen_options=self.survey_choices[self.current_page.index-1]
        answer_type=self.current_page.getAnswerType()
        if answer_type in ("Checkbox","Radio","Two options"):
            def addOption(new_option_value):
                is_chosen=new_option_value in self.chosen_options
                color=colors[0]
                if is_chosen:
                    color="blue"

                F_option=F(self.F_options)
                if answer_type=="Checkbox":
                    Var_checkbox=tk.IntVar()
                    Var_checkbox.set(is_chosen)
                    cd=lambda: Var_checkbox
                    new_option=C(F_option, variable=Var_checkbox, text=new_option_value, disabledforeground="black", bg=color, state="disabled", command=cd)

                else:
                    if self.chosen_options:
                        self.Var_radio.set(self.chosen_options[0])
                    new_option=R(F_option, variable=self.Var_radio, value=new_option_value, text=new_option_value, disabledforeground="black", bg=color, state="disabled")

                new_option.pack(side="left")
                F_option.pack(fill="x", pady=2)

            for value in self.current_page.getAvailableOptions():
                addOption(value)
        
        elif answer_type=="Multiline":
            if self.chosen_options:
                multilineLabel(self.F_options, self.chosen_options[0], bg="blue").pack(fill='x')

        else:
            if self.chosen_options:
                L(self.F_options, text=self.chosen_options[0], font=app.font, bg="blue").pack(fill='x')
        
        page_index=self.current_page.index
        if self.corrected_submissions[page_index] < len(self.submissions):
            F_validation=F(self.F_options)
            def validate(is_valid):
                if is_valid:
                    self.survey_valid_choices[page_index].append(deepcopy(self.chosen_options))
                self.corrected_submissions[page_index]+=1
                if self.corrected_submissions[page_index] < len(self.submissions):
                    self.survey_choices=self.submissions[self.corrected_submissions[page_index]]

                self.F_options=F(self.F_in_body)
                self.F_options.pack(fill='x', pady=24)
                self.displayCurrentPage()

            B(F_validation, text="INVALID", command=lambda: validate(0)).pack(side="left")
            B(F_validation, text="VALID", command=lambda: validate(1)).pack(side="right")
            F_validation.pack(fill='x')

    def closeWindow(self):
        for i in range(1, self.survey.getLength()):
            page=self.survey.getPage(i)
            if not page.auto_corrected:
                page.valid_options=self.survey_valid_choices[i]
        app.openNavigationWindow()


class App():
    def __init__(self):
        self.version="2.0"
        self.database_file_name="vey-DB.bin"
        self.font=("Consolas", 10, "bold")
        self.navigation_value="MAKE"
        self.loadDatabaseFrom(self.database_file_name)
        
        self.W_width="675"
        self.W_height="510"
        
        self.root=tk.Tk()
        self.root.geometry(self.W_width +'x'+ self.W_height)
        
        self.F_root=tk.Frame(self.root)

    def loadDatabaseFrom(self, db_file_path="vey-DB.bin"):
        self.database=Database()
        return
        with open(db_file_path, "rb") as db_file:
            self.database=pckl.load(db_file)
        print("LOADED")
    
    def saveDatabaseAs(self, db_file_name="vey-DB.bin"):
        return
        with open(db_file_name, "wb") as db_file:
            pckl.dump(self.database, db_file)
        print("SAVED")
    
    def run(self):
        self.openStartWindow()
        self.root.mainloop()

    # - - - - WINDOWS - - - -
    def openStartWindow(self):
        self.F_root.destroy()
        start_window=StartWindow()
        self.F_root=start_window.root
        self.F_root.pack(fill="both", expand=1)

    def openNavigationWindow(self):
        self.F_root.destroy()
        navigation_window=NavigationWindow()
        self.F_root=navigation_window.root
        self.F_root.pack(fill="both", expand=1)

    def openMakingWindow(self, survey):
        self.F_root.destroy()
        making_window=MakingWindow(survey)
        self.F_root=making_window.root
        self.F_root.pack(fill="both", expand=1)

    def openTakingWindow(self, survey):
        self.F_root.destroy()
        taking_window=TakingWindow(survey)
        self.F_root=taking_window.root
        self.F_root.pack(fill="both", expand=1)

    def openCorrectionWindow(self, survey, survey_choices):
        self.F_root.destroy()
        correction_window=CorrectionWindow(survey, survey_choices)
        self.F_root=correction_window.root
        self.F_root.pack(fill="both", expand=1)

    def openCorrectingWindow(self, survey):
        self.F_root.destroy()
        correcting_window=CorrectingWindow(survey)
        self.F_root=correcting_window.root
        self.F_root.pack(fill="both", expand=1)

    def openInsightWindow(self, survey_title):
        self.missingfeature()
    
    def getSurveyFromDatabase(self, survey_title):
        self.database.addSurveyTo(self.database.getSurvey(survey_title), "take")
    def getSurveyFromLocalStorage(self, path):
        self.missingfeature()

    def removeTakeSurvey(self, survey_title):
        self.database.removeSurveyFrom(survey_title, "take")
    def removeMakeSurvey(self, survey):
        self.database.removeSurveyFrom(survey, "making")

    def publishSurvey(self, survey_title):
        print(survey_title)
        published_survey=deepcopy(self.database.getSurveyFrom(survey_title, "making"))
        if self.database.hasSurvey(survey_title):
            self.database.updateSurveyIn(published_survey, survey_title, "surveys")
            self.database.updateSurveyIn(published_survey, survey_title, "made")
        else:
            self.database.addSurveyTo(published_survey, "surveys")
            self.database.addSurveyTo(published_survey, "made")
        app.exportSurvey(published_survey)

    def exportChoices(self, survey, survey_choices):
        title=survey.getTitle()
        data=(title, survey_choices)
        file_name="#CHOICES of " + title + ".bin"
        with open(file_name, "wb") as f:
            pckl.dump(data, f)
        self.message_window("Survey choices were successfully printed by the name :\n"+file_name)

    def importSurveyChoices(self, file_name):
        try:
            with open(file_name, "rb") as f:
                data=pckl.load(f)
            assert isinstance(data, tuple) and isinstance(data[0], str) and isinstance(data[1], tuple)
        except Exception as e:
            app.message_window("Oops ! "+e.__str__())
        else:
            self.database.submitToSurvey(data[0], data[1])
            self.message_window("Survey choices were successfully imported !")

    def exportCorrection(self, survey, survey_valid_choices):
        title=survey.getTitle()
        data=(title, survey_valid_choices)
        file_name="#CORRECTION of " + title + ".bin"
        with open(file_name, "wb") as f:
            pckl.dump(data, f)
        self.message_window("Successfully printed by the name :\n"+file_name)

    def importCorrection(self, file_name):
        try:
            with open(file_name, "rb") as f:
                data=pckl.load(f)
            assert isinstance(data, tuple) and isinstance(data[0], str) and isinstance(data[1], list)
        except Exception as e:
            app.message_window("Oops ! "+e.__str__())
        else:
            survey=self.database.getSurvey(data[0])
            survey_valid_choices=data[1]
            for i in range(1, survey.getLength()):
                page=survey.getPage(i)
                if i in survey_valid_choices:
                    page.valid_options=survey_valid_choices[i]
            
            self.message_window("Successfully imported !")

    def exportSurvey(self, survey):
        file_name= survey.getTitle() + ".bin"
        with open(file_name, "wb") as f:
            pckl.dump(survey, f)
        self.message_window("Survey was successfully printed by the name :\n"+file_name)

    def importSurvey(self, file_name):
        try:
            with open(file_name, "rb") as f:
                data=pckl.load(f)
            assert isinstance(data, Survey)
        except Exception as e:
            app.message_window("Oops ! "+e.__str__())
        else:
            self.database.addSurveyTo(data, "surveys")
            self.database.addSurveyTo(data, "making")
            self.openTakingWindow(data)

    def message_window(self, message_text):
        W_message=tk.Tk()

        F_message=F(W_message)
        lines=message_text.split('\n')
        for i, line in enumerate(lines):
            L(F_message, text=line, font=self.font).grid(row=i, column=0, sticky='W')
        F_message.pack(padx=8, pady=8)

        F_events=F(W_message)
        B(F_events, text="OK", font=self.font, command=W_message.destroy, width=4).pack(side="right", padx=5, pady=5)
        F_events.pack(fill='x')

        W_message.mainloop()

    def missingfeature(self):
        self.message_window("Feature is not available yet !")



codes=[str(i) for i in range(10)]
def generatedCode():
    code=''
    for i in range(3):
        code+=randchoice(codes)
    return code

app=App()
app.run()
