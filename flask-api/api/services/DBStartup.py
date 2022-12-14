from api.models.Users import User, Role, Group
from api.models.Posts import Post, PostLike, PostComment
from api.models.db import db
from api.models.Events import Event
from api.models.Messages import Message
import logging
from passlib.hash import sha256_crypt
from datetime import datetime

def seed_db():
    """Initial seeding of database on application start up."""

    if Role.query.count() == 0:

        admin_role = Role(
            id=1,
            name="Admin",
            description="Role for users that manage an organizations instance of the platform.",
        )

        db.session.add(admin_role)
        db.session.commit()
        logging.warning(f"No roles found, default roles created.")

    if User.query.count() == 0:
        password = sha256_crypt.encrypt("password")
        admin = User(
            first_name="Tom",
            last_name="Admin",
            grad_year="2024",
            major="ADMINISTRATION",
            username="Myspace Tom",
            email="admin@email.com",
            password=password,
        )
        admin.roles.append(admin_role)
        #user_datastore.add_role_to_user(admin, "Admin")
        db.session.add(admin)
        db.session.commit()
        logging.warning(
            f"No admin found, default admin account made. Make sure default credentials are changed."
        )
    #everything past here is extra for testing

    if User.query.count() == 1:
        password = sha256_crypt.encrypt("password")
        user1 = User(
            first_name="Bob",
            last_name="Smith",
            grad_year="2026",
            major="Basket Weaving",
            username="TheBob",
            email="bob@email.com",
            password=password,
        )
        db.session.add(user1)
        db.session.commit()

    if User.query.count() == 2:
        password = sha256_crypt.encrypt("password")
        user2 = User(
            first_name="John",
            last_name="Second",
            grad_year="2027",
            major="Economics",
            username="TheJohn",
            email="john@email.com",
            password=password,
        )
        db.session.add(user2)
        db.session.commit()

    if User.query.count() == 3:
        password = sha256_crypt.encrypt("password")
        user3 = User(
            first_name="Josh",
            last_name="Third",
            grad_year="2024",
            major="Political Science",
            username="cooljosh",
            email="josh@email.com",
            password=password,
        )
        db.session.add(user3)
        db.session.commit()

    if User.query.count() == 4:
        password = sha256_crypt.encrypt("password")
        user4 = User(
            first_name="Mike",
            last_name="Fourth",
            grad_year="2025",
            major="Criminal Justice",
            username="Coolguyjohn",
            email="mike@email.com",
            password=password,
        )
        db.session.add(user4)
        db.session.commit()

    if User.query.count() == 5:
        password = sha256_crypt.encrypt("password")
        user5 = User(
            first_name="Walter",
            last_name="Fifth",
            grad_year="2025",
            major="Chemistry",
            username="WalterWhite",
            email="walter@email.com",
            password=password,
        )
        db.session.add(user5)
        db.session.commit()

        # adding user 1 and 2 as friends
        add = user1.add_friend(user2)
        db.session.add(add)
        db.session.commit()
        add1 = user2.add_friend(user1)
        db.session.add(add1)
        db.session.commit()
        add = user2.add_pending_friend(user1)
        add1 = user1.add_pending_friend(user2)
        db.session.add(add)
        db.session.add(add1)
        db.session.commit()

        # adding user 1 and 3 as friends
        add = user1.add_friend(user3)
        db.session.add(add)
        db.session.commit()

        add1 = user3.add_friend(user1)
        db.session.add(add1)
        db.session.commit()

        add = user3.add_pending_friend(user1)
        add1 = user1.add_pending_friend(user3)
        db.session.add(add)
        db.session.add(add1)
        db.session.commit()

        # adding user 1 and 5 as friends
        add = user1.add_friend(user5)
        db.session.add(add)
        db.session.commit()

        add1 = user5.add_friend(user1)
        db.session.add(add1)
        db.session.commit()

        add = user5.add_pending_friend(user1)
        add1 = user1.add_pending_friend(user5)
        db.session.add(add)
        db.session.add(add1)
        db.session.commit()

        # adding user 2 and 4 as friends
        add = user2.add_friend(user4)
        db.session.add(add)
        db.session.commit()

        add1 = user4.add_friend(user2)
        db.session.add(add1)
        db.session.commit()

        add = user4.add_pending_friend(user2)
        add1 = user2.add_pending_friend(user4)
        db.session.add(add)
        db.session.add(add1)
        db.session.commit()

        # adding user 4 and 5 as friends
        add = user4.add_friend(user5)
        db.session.add(add)
        db.session.commit()

        add1 = user5.add_friend(user4)
        db.session.add(add1)
        db.session.commit()

        add = user4.add_pending_friend(user5)
        add1 = user5.add_pending_friend(user4)
        db.session.add(add)
        db.session.add(add1)
        db.session.commit()

    if Post.query.count() == 0:
        post1 = Post(
            title="Just signed up",
            content="Just signed up this app is so cool",
            user_id=user2.id,
        )

        db.session.add(post1)
        db.session.commit()

    if Post.query.count() == 1:
        post2 = Post(
            title="Basketball Game",
            content="Anybody want to go to the basketball game?",
            user_id=user3.id,
        )

        db.session.add(post2)
        db.session.commit()

    if Post.query.count() == 2:
        post3 = Post(
            title="I need a basket weaving tutor",
            content="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut",
            user_id=user1.id,
        )

        db.session.add(post3)
        db.session.commit()

    if Post.query.count() == 3:
        post4 = Post(
            title="Can anybody give me a ride to class?",
            content="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut",
            user_id=user4.id,
        )

        db.session.add(post4)
        db.session.commit()

    if Post.query.count() == 4:
        post5 = Post(
            title="When do we register for classes??",
            content="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut",
            user_id=user5.id,
        )

        db.session.add(post5)
        db.session.commit()

    if Post.query.count() == 5:
        post6 = Post(
            title="This class is so cool",
            content="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut",
            user_id=user3.id,
        )

        db.session.add(post6)
        db.session.commit()

    if Post.query.count() == 6:
        post7 = Post(
            title="Anybody want to go golfing this weekend?",
            content="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut",
            user_id=user5.id,
        )

        db.session.add(post7)
        db.session.commit()

    if PostLike.query.count() == 0:
        post_like1 = PostLike(post_id=post1.id, user_id=user1.id)
        db.session.add(post_like1)
        db.session.commit()

    if PostLike.query.count() == 1:
        post_like2 = PostLike(post_id=post1.id, user_id=user4.id)
        db.session.add(post_like2)
        db.session.commit()

    if PostLike.query.count() == 2:
        post_like3 = PostLike(post_id=post3.id, user_id=user3.id)
        db.session.add(post_like3)
        db.session.commit()

    if PostComment.query.count() == 0:
        post_comment1 = PostComment(
            post_id=post1.id,
            user_id=user1.id,
            text="Yeah its really cool, i wish i could donate them money",
        )
        db.session.add(post_comment1)
        db.session.commit()

    if PostComment.query.count() == 1:
        post_comment2 = PostComment(
            post_id=post3.id,
            user_id=user5.id,
            text="I could help you, I have the best basket weaves at school",
        )
        db.session.add(post_comment2)
        db.session.commit()

    if Message.query.count() == 0:
        message1 = Message(
            sender_id=user2.id,
            recipient_id=user1.id,
            body="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut",
        )

        db.session.add(message1)
        db.session.commit()

    if Message.query.count() == 1:
        message1 = Message(
            sender_id=user1.id, recipient_id=user2.id, body="WHAT IS THAT???"
        )

        db.session.add(message1)
        db.session.commit()

    if Group.query.count() == 0:
        group1 = Group(
            name="Computer Club",
            description="Group for people who like computers.",
            invite_only=False
        )

        group1.make_owner(user=user1, current_user=None)
        db.session.add(group1)
        db.session.commit()

        user3.join_group(group1)
        user4.join_group(group1)

    if Post.query.count() == 7:
        post8 = Post(
            title="Computer Club First Post",
            content="Computers are cool",
            user_id=user5.id,
            group_id=group1.id
        )

        db.session.add(post8)
        db.session.commit()

    if Event.query.count() == 0:

        event_time = "12/8/2022 5:00"
        
        timestamp = datetime.strptime(event_time, "%m/%d/%Y %H:%M")
        event1 = Event(
            name="End of the world",
            description="The mayan calendar foretold the ending of our world on this day. Join for the doomsday party!",
            time=timestamp,
            owner_id=4
        )

        db.session.add(event1)
        db.session.commit()
        event1.join_event(user3)
        event1.join_event(user5)

