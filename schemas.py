from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    email = fields.String(required=True, validate=[validate.Length(max=50)])
    username = fields.String(required=True, validate=[validate.Length(max=50)])
    password = fields.String(required=True, load_only=True, validate=[validate.Length(max=50)])


class PostSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=[validate.Length(max=255)])
    content = fields.String(required=True, validate=[validate.Length(max=500)])
    publication_datetime = fields.DateTime()
    author_id = fields.String(dump_only=True, validate=[validate.Length(max=50)])
    message = fields.String(dump_only=True)


class PostSchemaForUpdate(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(validate=[validate.Length(max=255)])
    content = fields.String(validate=[validate.Length(max=500)])
    publication_datetime = fields.DateTime()
    author_id = fields.String(dump_only=True, validate=[validate.Length(max=50)])
    message = fields.String(dump_only=True)


class CommentSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=[validate.Length(max=255)])
    content = fields.String(required=True, validate=[validate.Length(max=255)])
    publication_datetime = fields.DateTime()
    author_id = fields.String(dump_only=True, validate=[validate.Length(max=50)])
    post_id = fields.Integer(dump_only=True)
    message = fields.String(dump_only=True)


class CommentSchemaForUpdate(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(validate=[validate.Length(max=255)])
    content = fields.String(validate=[validate.Length(max=255)])
    publication_datetime = fields.DateTime()
    author_id = fields.String(dump_only=True, validate=[validate.Length(max=50)])
    post_id = fields.Integer(dump_only=True)
    message = fields.String(dump_only=True)


