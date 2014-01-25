from google.appengine.api import users
from google.appengine.ext import db
from datetime import timedelta, datetime
import webapp2,cgi,jinja2,os,random

JINJA_ENVIRONMENT = jinja2.Environment(
loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True)

ADD_POINT = 1;
SPECIAL_KEY = '71417320de826ebc9688de68c8232383'

class Player(db.Model):
	name = db.StringProperty()
	points = db.IntegerProperty()
	updateTime = db.DateTimeProperty()

class LeadersPage(webapp2.RequestHandler):

	def get(self):
		topPlayers = db.GqlQuery("SELECT * FROM Player WHERE points>0 ORDER BY points DESC")
		leaderboard_template_values = {
		'topplayers':topPlayers
		}
		leaderboard_template = JINJA_ENVIRONMENT.get_template('templates/leaderboard.html')
		self.response.write(leaderboard_template.render(leaderboard_template_values))		

class AddPoint(webapp2.RequestHandler):

	def get(self):
		IS_VALID = False
		if(self.request.get('special')):
			special = str(self.request.get('special'))
			if(special==SPECIAL_KEY):
				user = users.get_current_user()
				if user:
					allUsers = matchingUsersFor(user)
					print len(allUsers)
					if len(allUsers) == 0:
						print "[D]-New User"
						player = Player(name=user.email(),points=ADD_POINT)
						IS_VALID = True
					else:
						print "[D]-Updated User"
						player = allUsers[0]
						player.points += ADD_POINT
						if(player.updateTime):
							oldUpdate = player.updateTime
							timeDifference = datetime.now() - oldUpdate
							checkTime = random.randint(1800,3600)
							if timeDifference.seconds > checkTime:
								IS_VALID = True
						else:
							IS_VALID = True
					if(IS_VALID):
						player.updateTime = datetime.now()
						player.put()
						point_template_values = {
						'amount':ADD_POINT
						}
						point_template = JINJA_ENVIRONMENT.get_template('templates/point.html')
						self.response.write(point_template.render(point_template_values))
					else:
						error_template = JINJA_ENVIRONMENT.get_template('templates/error.html')
						self.response.write(error_template.render())						
				else:
					self.redirect(users.create_login_url(self.request.uri))
			else:
				self.redirect('/')
		else:
			self.redirect('/')




class UserProfile(webapp2.RequestHandler):

	def get(self):
		currentUser = users.get_current_user()
		if currentUser:
			players = matchingUsersFor(currentUser)
			if(len(players)==1):
				player = players[0]
			else:
				player = Player(name=currentUser.email(),points=0,nickname=currentUser.nickname())
				player.put()			
			user_template_values = {
				'username':player.name,
				'points':player.points,
				'logout_url': users.create_logout_url("/"),
				'level': getLevel(player.points)
				}		
			user_template = JINJA_ENVIRONMENT.get_template('templates/user.html')
			self.response.write(user_template.render(user_template_values))	

		else:
			self.redirect(users.create_login_url(self.request.url))

class PurgeMain(webapp2.RequestHandler):

	def get(self):
		playerKeys = Player.all(keys_only=True);
		for key in playerKeys:
			db.delete(key)


def getLevel(points):

	if 0<=points<=5:
		return 'Novice Sanitarian'
	elif 6<=points<=10:
		return 'Regular Sanitarian'
	elif 11<=points<=15:
		return 'Master Sanitarian'
	elif 16<=points<=20:
		return 'Novice Trashmaster'
	elif 21<=points<=25:
		return 'Regular Trashmaster'
	elif 26<=points<=30:
		return 'Master Trashmaster'
	elif points>=31:
		return 'Emperor Rubbish'



def matchingUsersFor(user):
	return db.GqlQuery("SELECT * FROM Player WHERE name=:1",user.email()).fetch(1)



application = webapp2.WSGIApplication({
	('/',LeadersPage),
	('/point',AddPoint),
	('/user',UserProfile),
	('/purgemain',PurgeMain)
},debug=True)