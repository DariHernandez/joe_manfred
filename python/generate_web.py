#! python3

import os, bs4, csv, sys
from PIL import Image

class Generate (): 
    """
    Generate static html files for ther web page
    """

    def __init__ (self, path_web): 
        """
        Constructor of the class. Get path of all documents
        """

        self.path_web = path_web
        self.path_python = os.path.dirname (__file__)
        self.path_templates = os.path.join (self.path_python, "templates html")


        # Index files
        self.index_file_template  = open(os.path.join (self.path_templates, "index-template.html"), "r")
        self.index_file = open(os.path.join (self.path_web, "index.html"), "w")

        # Board files
        self.board_file_template  = open(os.path.join (self.path_templates, "board-template.html"), "r")
        self.board_best = open(os.path.join (self.path_web, "board-best.html"), "w")
        self.board_all = open(os.path.join (self.path_web, "board-all.html"), "w")
        self.board_videos = open(os.path.join (self.path_web, "board-videos.html"), "w")

        # Article files
        self.article_file_template  = open(os.path.join (self.path_templates, "article-template.html"), "r")
        self.articles_folder = os.path.join (self.path_web, "articles")

        # Data CSV
        csv_file = open (os.path.join (os.path.dirname (__file__), "data.csv"))
        self.data = self.__get_data (csv_file)

    
    def __get_data (self, file): 
        """
        Return dara from csv file
        """

        reader_csv = csv.reader (file)
        data = list(reader_csv)

        return data

    def index (self): 
        """
        Generate file "index.html", with the correct files and information
        """

        print ("Generating index...")


        # all lines of the template html file
        lines_html = []

        # get position for insert html code
        best_position = 0
        all_position = 0
        videos_position = 0

        counter_line = 0
        elements_counter = 0

        # Read and save each line of html file
        for line in self.index_file_template.readlines():
            
            lines_html.append (line)

            # Identify speicic line in the text
            elemnt = '<div class="articles-container">'

            # Get position of each line for each section
            if line.strip() == elemnt: 
                elements_counter += 1

                if elements_counter == 1:
                    best_position = counter_line + 1
                
                if elements_counter == 2:
                    all_position = counter_line + 1
                
                if elements_counter == 3:
                    videos_position = counter_line + 1
        
            counter_line += 1

        # Position of each section value inside the data file
        index_section_best = 5
        index_section_all = 4
        index_section_videos = 3

        # Get all text and formated sections
        html_text = []
        # Header
        html_text += (lines_html [:best_position]) 
        # Section Best 
        html_text += (self.__get_articles_section(index_section_best, max_10 = True))
        # Best - All intersection
        html_text += (lines_html [best_position:all_position])
        # Section All
        html_text += (self.__get_articles_section(index_section_all, max_10 = True))
        # Alll - Videos intersection
        html_text += (lines_html [all_position:videos_position])
        # Section videos
        html_text += (self.__get_articles_section(index_section_videos, max_10 = True))
        # footer
        html_text += (lines_html [videos_position:])

        # Write information in file
        for line in html_text: 
            self.index_file.write ("\n" + line.rstrip())


    def __get_articles_section (self, section, max_10 = False): 
        """
        Return a list with html text lines, fromated and with information of each article of the section
        """

        articles_html = []

        # Extrat first 10 row of data
        max_articles = len(self.data) - 1
        article_counter = 0
        articles_section = 0
        while article_counter <= max_articles:

            # Stop program if it request only ten articles | detect if it is index or board page
            if max_10: 
                video_size = 'width="auto" height="100%"'
                if articles_section >= 10:
                    break
            else: 
                video_size = 'width="100%" height="auto"'

                
            if self.data[article_counter][section].strip().lower() == 'true':
                data_article = self.data[article_counter]
                articles_section += 1

                # Save variables
                src = "imgs/small/" + data_article[2]
                scr_video = "video/" + data_article[2][:data_article[2].rfind (".")] + ".mp4"
                name = data_article[0]
                link = "articles/" + str(data_article[0]).replace (" ", "-") + ".html"
                
                # verify if section article is video or image
                if section == 3: 
                    class_article = "video"
                else: 
                    class_article = "img"
    

                # Generate article html
                articles_html.append ('                <div class="article-container button">')
                articles_html.append ('                    <article>')
                articles_html.append ('                        <figure class={}>'.format(class_article))
                articles_html.append ('                            <img src="{}"  alt="">'.format (src))

                # If its videos, ad preview
                if class_article == "video": 
                    articles_html.append ('                            <video src="{}" {} type="video/mp4" autoplay muted loop></video>'.format (scr_video, video_size))



                articles_html.append ('                        </figure>')
                articles_html.append ('                        <h3>{}</h3>'.format(name.title()))
                articles_html.append ('                   </article>')
                articles_html.append ('                </div>')

            article_counter +=1 

        return articles_html
    
    def boards (self): 
        """
        Generate ALL boards html files
        """

        print ("Generating boards...")

        # Position of each section value inside the data file
        data_index_board_best = 5
        data_index_board_all = 4
        data_index_board_videos = 3

        # Generate each board
        self.__board (data_index_board_best, self.board_best)
        self.__board (data_index_board_all, self.board_all)
        self.__board (data_index_board_videos, self.board_videos)

    def __board (self, data_index, board_file):
        """
        Generate a board html file, with the correct format and information
        """


        # all lines of the template html file
        lines_html = []

        # Line of the board in the html file
        position_board = 0

        counter_line = 0
        for line in self.board_file_template.readlines():

            lines_html.append (line)

            # Identify speicic line in the text
            elemnt = '<main>'

            if line.strip() == elemnt: 
                position_board = counter_line + 1
            
            counter_line+=1

        # Move the pointer to the start of the file
        self.board_file_template.seek (0)

        # Get all text and format sections
        html_text = []

        # Header
        html_text += (lines_html [:position_board]) 

        # Board
        html_text += (self.__get_board (data_index))

        # Footer
        html_text += (lines_html [position_board:]) 

        # Write information in file
        for line in html_text: 
            board_file.write ("\n" + line.rstrip())


    def __get_board (self, data_index): 
        """
        Reurn a list with html text lines, formated and with image of the boards
        """

        articles_html = []

        # get articles of the specificv section
        artiles_section =  self.__get_articles_section (data_index, max_10 = False)

        # Get data for videos and gereate titles
        if data_index == 5: 
            # Title
            title = "My best works"

        elif data_index == 4: 
            # Title
            title = "All works"

        elif  data_index == 3: 
            # Title
            title = "Videos"

        
        # Add title and grid open
        articles_html.append ('        <h1>{}</h1>'.format (title))
        articles_html.append ('        <div id="board">')

        # Save articles of the column
        for article in artiles_section: 
            articles_html.append (article)


        # Add of board close
        articles_html.append ('        </div>')

        return articles_html

    def articles (self): 
        """
        Generate each article of the data base
        """

        print ("Generating articles...")

        for article in self.data: 

            # Skip header 
            if self.data.index (article) >= 1: 


                name = article [0]
                date = article [1]
                file = article [2]
                video = article [3]
                ytframe = article[7]
                description = article [6]

                # all lines of the template html file
                lines_html = []

                # get position for insert html code
                position = 0

                counter_line = 0

                # Read and save each line of html file
                for line in self.article_file_template.readlines():
                
                    lines_html.append (line)

                    # Identify speicic line in the text
                    elemnt = '<main>'

                    # Get position of each line for main section
                    if line.strip() == elemnt: 
                        position = counter_line + 1
                    
                    counter_line += 1
                
                # Retornar puntero al comienzo del documento
                self.article_file_template.seek (0)
                
                # Get all text and formated sections
                html_text = []

                # Header
                html_text += (lines_html [:position]) 
                
                # Article
                article_lines = self.__article (name, date, description, file, video, ytframe)
                html_text += article_lines

                # Footer
                html_text += (lines_html [position:]) 

                # Write data in file
                article_name = name.replace (" ", "-") + ".html"
                article_file = open (os.path.join (self.articles_folder, article_name), "w")
                for line in html_text: 
                    article_file.write ("\n" + line.rstrip())


    def __article (self, name, date, description, file, video, ytframe):
        """
        Generate article html text with specific information
        """

        article_html = []

        # Verify video  or image article
        if str(video).lower().strip() == "true":
            
            # Name of the image
            name_image = name[:name.lower().find(" speed")]

            article_html.append ('        <h1>{}</h1>'.format (name.title()))
            article_html.append ('        <h3>Date: {}</h3>'.format(date))
            article_html.append ('        <p>{}</p>'.format(description))

            article_html.append ('            <div class="video-container">')
            article_html.append ('                <figure class="main-video">')
            article_html.append ('                    {}'.format (ytframe))
            article_html.append ('                </figure>')
            article_html.append ('                <div class="final-image button">')
            article_html.append ('                    <h3>Final image:</h3>')
            article_html.append ('                    <a href="{}">'.format (name_image.replace (" ", "-") + ".html"))
            article_html.append ('                       <figure>')
            article_html.append ('                            <img src="{}" alt="">'.format ("../imgs/small/" + name_image + ".jpg"))
            article_html.append ('                        </figure>')
            article_html.append ('                    </a>')
            article_html.append ('                </div>')
            article_html.append ('            </div>')
        else: 

            # Size of the image
            img_path = os.path.join(self.path_web, "imgs", "all", file)
            img = Image.open (img_path)
            width, height = img.size
            size = "{} x {} px".format (width, height)

            # Get image url
            link = "../imgs/all/" + file

            article_html.append ('        <h1>{}</h1>'.format (name.title()))
            article_html.append ('        <h3>Date: {}</h3>'.format(date))
            article_html.append ('        <h3>Size: {}</h3>'.format(size))
            article_html.append ('        <p>{}</p>'.format(description))
            article_html.append ('        <div class="main-image-wrapper">')
            article_html.append ('            <figure class="main-image max-height">')
            article_html.append ('                <div class="text-container">')
            article_html.append ('                    <h3 > > Click to resize < </h3>')
            article_html.append ('                </div>')
            article_html.append ('                <img src="{}" alt="">'.format(link))
            article_html.append ('            </figure>')

        article_html.append ('        </div>')

        return article_html




        
