from google.appengine.api import users
from google.appengine.ext import db
from datetime import timedelta, datetime
import webapp2,cgi,jinja2,os,random

JINJA_ENVIRONMENT = jinja2.Environment(
loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True)

ADD_POINT = 1;
SPECIAL_KEY = '308ff32611ad0a6718c7b9d69c6b2e69282d282fedb656db02482430ad38052fe7c2d6ffc16649fc08bfa915321bdff440590e5c953faa51c73fa796c65db6e9'

class Player(db.Model):
	nickname = db.StringProperty()
	name = db.StringProperty()
	points = db.IntegerProperty()

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
		IS_VALID = True
		if(self.request.get('k')):
			special = str(self.request.get('k'))
			if(special==SPECIAL_KEY):
				user = users.get_current_user()
				if user:
					allUsers = matchingUsersFor(user)
					print len(allUsers)
					if len(allUsers) == 0:
						print "[D]-New User"
						player = Player(name=user.email(),points=ADD_POINT,nickname=user.nickname())
					else:
						print "[D]-Updated User"
						player = allUsers[0]
						if(player.nickname is None):
							player.nickname = user.nickname()
						player.points += ADD_POINT
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
		emailWinner()
		playerKeys = Player.all(keys_only=True)
		for key in playerKeys:
			db.delete(key)

def emailWinner():
	
	maxPoints = None
	try: 
		maxPoints = Player.all().order('-points').get().points
	except AttributeError:
		print "[D]-No Users..."
	if maxPoints is not None:
		winners = db.GqlQuery("SELECT * FROM Player WHERE points=:1",maxPoints)
		for winner in winners:
			winnerEmail = winner.name
			message  = mail.EmailMessage(sender="Recycled Admin <dev.tahoma@mysummitps.org>", subject="You've won Recycled!")
			message.to = winnerEmail
			message.body="""
			Congratulations %s for winning this month's Recycled! \n 
			
			---- 
			This was an automated message sent by Lamar the bot. Do not reply to this email.
			(Service still in beta)
			""" % winnerEmail
			message.send()
				

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