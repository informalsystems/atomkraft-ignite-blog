---- MODULE blog ----
EXTENDS Apalache, Variants, Sequences, Integers

(*
@typeAlias: blog = {creator: Str, title: Int, body: Int};
@typeAlias: action = Post($blog) | Query(Seq($blog)) | Init(Int);
*)
typedefs == TRUE

USERS == {"alice", "bob"}
TITLES == 1..1000
BODIES == 1..1000

VARIABLES
    \* @type: Seq($blog);
    blogs,
    \* @type: $action;
    action

Init ==
    /\ blogs = <<>>
    /\ action = Variant("Init", 0)

\* @type: ($blog) => $action;
PostAction(_blog) == Variant("Post", _blog)

\* @type: () => $action;
QueryAction == Variant("Query", blogs)

PostNext ==
    \E creator \in USERS, title \in TITLES, body \in BODIES:
        LET b == [creator |-> creator, title |-> title, body |-> body] IN
        /\ blogs' = Append(blogs, b)
        /\ action' = PostAction(b)

QueryNext ==
    /\ UNCHANGED <<blogs>>
    /\ action' = QueryAction

Next ==
    \/ PostNext
    \/ QueryNext


\* @type: (Seq({blogs: Seq($blog), action: $action})) => Bool;
TraceLen(trace) == ~(
    Len(trace) = 5
)

View == VariantTag(action)

====